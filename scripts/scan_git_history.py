#!/usr/bin/env python3
"""Lightweight common-secret and private-path scan of ALL locally reachable Git blobs.

This is intentionally conservative and not a replacement for specialist
high-entropy scanners such as Gitleaks or legal/manual code review.
Prints only blob IDs and pattern types, never potential secret values.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys

PATTERNS = {
    "GitHub token": rb"(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})",
    "Google API key": rb"AIza[0-9A-Za-z_-]{32,}",
    "AWS access key": rb"(?:AKIA|ASIA)[A-Z0-9]{16}",
    "OpenAI-style token": rb"sk-[A-Za-z0-9_-]{20,}",
    "Slack token": rb"xox[baprs]-[A-Za-z0-9-]{20,}",
    "Private key header": rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "Private Colab Drive path": rb"/content/drive/MyDrive/[A-Za-z0-9_.-]",
}
REGEX = {name: re.compile(expression) for name, expression in PATTERNS.items()}

# Release gate: reject historically tracked raw data, trained weights, credential
# files, and binary/paper artifacts, even if later removed from the current tree.
# Check all reachable *commits*, not only HEAD.
SENSITIVE_SUFFIXES = (
    ".pt", ".pth", ".ckpt", ".npz", ".npy", ".tif", ".tiff",
    ".jpg", ".jpeg", ".png", ".pdf", ".zip", ".7z", ".h5",
    ".hdf5", ".onnx", ".pkl", ".pickle", ".parquet",
    ".pem", ".key", ".p12", ".pfx",
)
SENSITIVE_BASENAMES = (
    "credentials.json", "kaggle.json", "id_rsa", "id_ed25519",
)

def classify_sensitive_path(path: str) -> str | None:
    """Return a generic risk label; avoid printing personal/sensitive filenames."""
    norm = path.replace("\\", "/").lower()
    parts = norm.split("/")
    basename = parts[-1]
    if basename == ".env.example":
        return None
    if basename == ".env" or basename.startswith(".env."):
        return "environment/credential file"
    if basename in SENSITIVE_BASENAMES or basename.startswith("service_account"):
        return "credential/identity file"
    if any(p in {"secrets", "private", "raw_data", "datasets", "checkpoints", "weights"} for p in parts[:-1]):
        return "sensitive directory"
    if basename.endswith(SENSITIVE_SUFFIXES):
        return "binary/data/model/paper artifact"
    return None


def run_git(*args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args], capture_output=True, check=False,
    )
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed (exit {proc.returncode})")
    return proc.stdout

def scan(max_blob_bytes: int = 10_000_000) -> int:
    seen = set()
    hits = []
    oversized = []
    blobs_checked = 0
    # Inspect filenames in every reachable commit, including deleted/renamed files.
    sensitive_paths = set()
    commit_shas = run_git("rev-list", "--all").splitlines()
    for sha_bytes in commit_shas:
        sha = sha_bytes.decode("ascii")
        for path_bytes in run_git("ls-tree", "-r", "-z", "--name-only", sha).split(b"\x00"):
            if not path_bytes:
                continue
            path = path_bytes.decode("utf-8", errors="replace")
            label = classify_sensitive_path(path)
            if label:
                sensitive_paths.add((label, path))

    for line in run_git("rev-list", "--objects", "--all").splitlines():
        oid = line.split(b" ", 1)[0].decode("ascii")
        if oid in seen:
            continue
        seen.add(oid)
        if run_git("cat-file", "-t", oid).strip() != b"blob":
            continue
        size = int(run_git("cat-file", "-s", oid))
        if size > max_blob_bytes:
            oversized.append((oid[:12], size))
            continue
        data = run_git("cat-file", "-p", oid)
        blobs_checked += 1
        for name, rx in REGEX.items():
            if rx.search(data):
                hits.append((oid[:12], name))
    print(f"Scanned {blobs_checked} reachable Git blobs across all local refs.")
    for oid, kind in hits:
        print(f"FAIL: {oid}: possible {kind} (value suppressed)")
    for oid, size in oversized:
        print(f"REVIEW: {oid}: oversized blob ({size} bytes), skipped")
    print(f"Checked filenames across {len(commit_shas)} reachable commits.")
    for label in sorted({label for label, _ in sensitive_paths}):
        print(f"FAIL: historically tracked {label} (filenames suppressed)")

    if hits or oversized or sensitive_paths:
        return 1
    print("PASS: no configured token/key patterns, private Colab Drive paths, or historically tracked sensitive artifact filenames.")
    print("Caveat: pattern matching does not establish full secrets/PII clearance.")
    return 0

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--max-blob-bytes", type=int, default=10_000_000)
    a = p.parse_args()
    try:
        sys.exit(scan(a.max_blob_bytes))
    except (OSError, RuntimeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
