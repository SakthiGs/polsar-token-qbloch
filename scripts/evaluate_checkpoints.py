#!/usr/bin/env python3
"""Replay saved EXP37 checkpoints on the original held-out candidate cache.

This does NOT regenerate detector candidates from raw FPSD imagery.
Both cache and checkpoint weights must be obtained from the data owner;
they are intentionally not distributed in this repository.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from types import SimpleNamespace
from typing import Callable, Dict, Tuple

import numpy as np
import torch
import torch.nn as nn
from scipy.stats import wilcoxon
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb"
QUANTUM = "Token_Arch2Quantum_Fusion"
CLASSICAL = "Token_Arch2Control_Fusion"

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def get_registry():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code = next("".join(c["source"]) for c in notebook["cells"]
                if "class ThreeQubitUnitary(nn.Module)" in "".join(c.get("source", [])))
    cfg = SimpleNamespace(token_dim=8, q_layers=2, arch2_obs_dim=12,
                          control_hidden_a2=4, d_model=32, heads=4, dropout=.1,
                          patch_grid=6, fidelity_init_alpha=.1, fidelity_center=True)
    scope = {
        "torch": torch, "nn": nn, "np": np, "math": math,
        "Exp37Config": type("Exp37Config", (), {}),
        "Callable": Callable, "Dict": Dict, "Tuple": Tuple, "CFG": cfg
    }
    exec(compile(code, NOTEBOOK.name, "exec"), scope)
    return scope["MODEL_REGISTRY"], cfg

def replay(cache: Path, checkpoints: Path, output: Path, seeds, threads=3, batch_size=128):
    torch.set_num_threads(threads)
    with np.load(cache, allow_pickle=False) as data:
        rho = data["rho"]; tokens = data["tokens"]; labels = data["y"].astype(int)
    if rho.shape[0] != len(labels) or tokens.shape[0] != len(labels):
        raise ValueError("Misaligned validation arrays")
    if rho.shape[1:] != (36,3,3) or tokens.shape[1:] != (36,8):
        raise ValueError("Unexpected EXP37 held-out feature dimensions")
    if len(np.unique(labels)) != 2:
        raise ValueError("Held-out data must contain both classes")
    registry, cfg = get_registry()
    rows = []
    checksums = {}
    for model_name in (QUANTUM, CLASSICAL):
        for seed in seeds:
            path = checkpoints / f"{model_name}_seed{seed}.pt"
            state = torch.load(path, map_location="cpu", weights_only=True)
            if state.get("seed") != seed or state.get("model_name") != model_name:
                raise ValueError(f"Checkpoint identity mismatch: {path}")
            model = registry[model_name][0](cfg)
            model.load_state_dict(state["model_state"], strict=True)
            model.eval()
            probabilities = []
            with torch.no_grad():
                for start in range(0, len(labels), batch_size):
                    rr = torch.from_numpy(rho[start:start+batch_size])
                    tt = torch.from_numpy(tokens[start:start+batch_size])
                    probabilities.append(torch.sigmoid(model(rr, tt)).numpy())
            p = np.concatenate(probabilities)
            rows.append({
                "model": model_name, "seed": seed,
                "auc": float(roc_auc_score(labels, p)),
                "ap": float(average_precision_score(labels, p)),
                "f1": float(f1_score(labels, p>=.5))
            })
            checksums[path.name] = sha256_file(path)
    q = np.array([next(r["auc"] for r in rows if r["model"] == QUANTUM and r["seed"] == seed) for seed in seeds])
    c = np.array([next(r["auc"] for r in rows if r["model"] == CLASSICAL and r["seed"] == seed) for seed in seeds])
    diff = q - c
    report = {
        "provenance": "CPU evaluation of archived checkpoints and validation cache; not raw FPSD reproduction",
        "validation_cache_sha256": sha256_file(cache),
        "checkpoint_sha256": checksums,
        "candidate_count": int(len(labels)),
        "positive_candidates": int(labels.sum()),
        "negative_candidates": int(len(labels)-labels.sum()),
        "seeds": list(seeds),
        "quantum_auc_mean": float(q.mean()),
        "quantum_auc_sample_sd": float(q.std(ddof=1)),
        "classical_auc_mean": float(c.mean()),
        "classical_auc_sample_sd": float(c.std(ddof=1)),
        "paired_auc_mean_delta": float(diff.mean()),
        "wilcoxon_2s_p": float(wilcoxon(diff, alternative="two-sided").pvalue)
    }
    output.mkdir(parents=True, exist_ok=True)
    with (output/"checkpoint_replay_per_seed.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    (output/"checkpoint_replay_manifest.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="checkpoint_sha256"}, indent=2))
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--checkpoints", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("outputs/replay"))
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(42,52)))
    parser.add_argument("--threads", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=128)
    args = parser.parse_args()
    replay(args.cache, args.checkpoints, args.output, args.seeds, args.threads, args.batch_size)

if __name__ == "__main__":
    main()
