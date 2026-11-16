#!/usr/bin/env python3
"""Audit COCO train/validation image identity and annotations for FPSD.

Comparison uses normalized *filenames*, not COCO image IDs, because COCO image
IDs are local to each annotation split and may legally overlap across splits.
Optional --train-dir/--val-dir verify the actual files are accessible.
Optional --hash-images hashes every image to support a full input provenance
manifest without copying image bytes into the repository.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def normalize_file_name(value):
    s = str(value).replace("\\", "/")
    path = PurePosixPath(s)
    if not s or path.is_absolute() or ".." in path.parts:
        raise ValueError("Invalid or unsafe COCO file_name")
    return path.as_posix()

def load_coco(path):
    p = Path(path)
    coco = json.loads(p.read_text(encoding="utf-8"))
    images = coco.get("images", [])
    annotations = coco.get("annotations", [])
    if not isinstance(images, list) or not isinstance(annotations, list):
        raise ValueError(f"Invalid COCO JSON structure: {p.name}")
    if not images:
        raise ValueError(f"No images in: {p.name}")
    image_ids = [im["id"] for im in images]
    original_names = [normalize_file_name(im["file_name"]) for im in images]
    folded_names = [n.casefold() for n in original_names]
    if len(set(image_ids)) != len(image_ids):
        raise ValueError(f"Duplicate COCO image IDs within {p.name}")
    if len(set(folded_names)) != len(folded_names):
        raise ValueError(f"Duplicate or case-colliding filenames within {p.name}")
    ids = set(image_ids)
    if any(ann.get("image_id") not in ids for ann in annotations):
        raise ValueError(f"Annotations reference absent images in {p.name}")
    return {
        "path": p, "name": p.name, "sha256": sha256_file(p),
        "image_ids": ids, "filenames": original_names,
        "folded_names": set(folded_names), "annotations": len(annotations),
        "image_count": len(images),
    }

def audit_images(base_dir, names, hash_images):
    folder = Path(base_dir).expanduser()
    if not folder.is_dir():
        raise FileNotFoundError(f"Missing image directory: {folder}")
    missing = []
    manifest = hashlib.sha256()
    for name in sorted(names):
        p = folder.joinpath(*PurePosixPath(name).parts)
        if not p.is_file():
            missing.append(name)
            continue
        if hash_images:
            manifest.update(name.encode("utf-8") + b"\t")
            manifest.update(sha256_file(p).encode("ascii") + b"\n")
    if missing:
        raise FileNotFoundError(f"{len(missing)} source images absent, first: {missing[:3]}")
    return {
        "files_verified": len(names),
        "full_image_set_sha256": manifest.hexdigest() if hash_images else None,
    }

def verify_splits(train_ann, val_ann, train_dir=None, val_dir=None, hash_images=False):
    t = load_coco(train_ann)
    v = load_coco(val_ann)
    overlap = t["folded_names"] & v["folded_names"]
    if overlap:
        raise ValueError(f"Train/val filename overlap ({len(overlap)}), examples: {sorted(overlap)[:3]}")
    if hash_images and (train_dir is None or val_dir is None):
        raise ValueError("--hash-images requires --train-dir and --val-dir")
    report = {
        "identity_rule": "case-folded image filename (COCO numeric IDs may be reused)",
        "train": {
            "annotation_file": t["name"], "annotation_sha256": t["sha256"],
            "images": t["image_count"], "annotations": t["annotations"],
        },
        "val": {
            "annotation_file": v["name"], "annotation_sha256": v["sha256"],
            "images": v["image_count"], "annotations": v["annotations"],
        },
        "overlapping_filenames": len(overlap),
        "overlapping_local_coco_image_ids": len(t["image_ids"] & v["image_ids"]),
        "limitations": "Does not detect image-content duplicates across distinct filenames unless images are hashed and content hashes examined",
    }
    if train_dir is not None:
        report["train"]["source_files"] = audit_images(train_dir, t["filenames"], hash_images)
    if val_dir is not None:
        report["val"]["source_files"] = audit_images(val_dir, v["filenames"], hash_images)
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-ann", type=Path, required=True)
    parser.add_argument("--val-ann", type=Path, required=True)
    parser.add_argument("--train-dir", type=Path)
    parser.add_argument("--val-dir", type=Path)
    parser.add_argument("--hash-images", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = verify_splits(args.train_ann, args.val_ann, args.train_dir, args.val_dir, args.hash_images)
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    print("PASS: no duplicated train/validation filenames in COCO annotations.")

if __name__ == "__main__":
    main()
