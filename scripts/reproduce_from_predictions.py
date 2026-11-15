#!/usr/bin/env python3
"""Reconstruct EXP37 tests from held-out per-candidate predictions.

Reads <model>_seed<N>.npz files produced by the canonical notebook. Required
arrays: prob and label; optional aligned image_id for image-cluster bootstrap.
No original imagery or weights are necessary once predictions exist.
"""
import argparse
import csv
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon
from sklearn.metrics import average_precision_score, roc_auc_score, f1_score

PRIMARY_Q = "Token_Arch2Quantum_Fusion"
PRIMARY_C = "Token_Arch2Control_Fusion"
NOENT = "Token_Arch2Quantum_Fusion_NoEnt"

def read_predictions(path, models, seeds):
    data = {}
    for model in models:
        for seed in seeds:
            filename = path / f"{model}_seed{seed}.npz"
            if not filename.is_file():
                raise FileNotFoundError(filename)
            with np.load(filename, allow_pickle=False) as z:
                probs = np.asarray(z["prob"], float)
                labels = np.asarray(z["label"], int)
                ids = np.asarray(z["image_id"], str) if "image_id" in z else np.array([], str)
                if "seed" in z and int(z["seed"]) != seed:
                    raise ValueError(f"Seed differs from filename: {filename}")
                if "model" in z and str(z["model"]) != model:
                    raise ValueError(f"Model differs from filename: {filename}")
            if probs.ndim != 1 or labels.ndim != 1 or len(probs) != len(labels):
                raise ValueError(f"Invalid prediction array shapes: {filename}")
            if not np.isfinite(probs).all() or ((probs < 0) | (probs > 1)).any():
                raise ValueError(f"Invalid probabilities in {filename}")
            if not set(np.unique(labels)).issubset({0, 1}):
                raise ValueError("Non-binary labels")
            if len(ids) not in (0, len(labels)):
                raise ValueError("Image IDs not aligned")
            data[model, seed] = (probs, labels, ids)
    y = next(iter(data.values()))[1]
    for probs, labels, ids in data.values():
        if not np.array_equal(labels, y):
            raise ValueError("Held-out labels are not identically ordered across runs")
    if len(np.unique(y)) != 2:
        raise ValueError("Held-out labels must have both classes")
    base_ids = next((value[2] for value in data.values() if len(value[2])), None)
    if base_ids is not None:
        for value in data.values():
            if not len(value[2]) or not np.array_equal(value[2], base_ids):
                raise ValueError("Image IDs missing or differently ordered across runs")
    return data, y, base_ids

def paired_bootstrap(a, b, y, reps, seed=20260619, ids=None):
    rng = np.random.default_rng(seed)
    differences = []
    if ids is not None:
        unique_ids = np.unique(ids)
        groups = {value: np.flatnonzero(ids == value) for value in unique_ids}
    for _ in range(reps):
        if ids is None:
            ix = rng.integers(0, len(y), size=len(y))
        else:
            chosen = rng.integers(0, len(unique_ids), size=len(unique_ids))
            ix = np.concatenate([groups[unique_ids[k]] for k in chosen])
        if len(np.unique(y[ix])) < 2:
            continue
        differences.append(roc_auc_score(y[ix], a[ix]) - roc_auc_score(y[ix], b[ix]))
    if not differences:
        raise ValueError("No valid bootstrap resamples")
    v = np.asarray(differences, float)
    low, high = np.quantile(v, [.025, .975])
    p_two = min(1.0, 2 * min((v <= 0).mean(), (v >= 0).mean()))
    return {
        "level": "image" if ids is not None else "candidate",
        "b_boot": len(v), "delta_mean": float(v.mean()),
        "ci_lo": float(low), "ci_hi": float(high), "boot_p_2s": float(p_two),
    }

def compute(path: Path, output: Path, seeds, bootstrap):
    models = (PRIMARY_Q, PRIMARY_C, NOENT)
    predictions, labels, ids = read_predictions(path, models, seeds)
    rows = []
    for model in models:
        for seed in seeds:
            probs = predictions[model, seed][0]
            rows.append({
                "model": model, "seed": seed, "auc": roc_auc_score(labels, probs),
                "ap": average_precision_score(labels, probs),
                "f1": f1_score(labels, probs >= .5),
            })
    qauc = np.array([next(r["auc"] for r in rows if r["model"] == PRIMARY_Q and r["seed"] == seed) for seed in seeds])
    cauc = np.array([next(r["auc"] for r in rows if r["model"] == PRIMARY_C and r["seed"] == seed) for seed in seeds])
    pvalue = float(wilcoxon(qauc - cauc, alternative="two-sided").pvalue)
    pooled = {model: np.stack([predictions[model, seed][0] for seed in seeds]).mean(axis=0) for model in models}
    boot_rows = []
    for a, b in ((PRIMARY_Q, PRIMARY_C), (NOENT, PRIMARY_C), (PRIMARY_Q, NOENT)):
        result = paired_bootstrap(pooled[a], pooled[b], labels, bootstrap)
        result["comparison"] = a + " - " + b
        boot_rows.append(result)
        if ids is not None:
            cluster = paired_bootstrap(pooled[a], pooled[b], labels, bootstrap, ids=ids)
            cluster["comparison"] = result["comparison"]
            boot_rows.append(cluster)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "per_seed.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with (output / "paired_bootstrap.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(boot_rows[0]))
        w.writeheader()
        w.writerows(boot_rows)
    print("Primary paired-seed AUC gain:", round(float((qauc - cauc).mean()), 6),
          "Wilcoxon two-sided p:", round(pvalue, 6))
    print("Candidate bootstrap:", boot_rows[0])
    if ids is None:
        print("No image-cluster CI: aligned image IDs are unavailable.")
    return rows, boot_rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("outputs/recomputed"))
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(42, 52)))
    parser.add_argument("--bootstrap", type=int, default=2000)
    args = parser.parse_args()
    compute(args.predictions, args.output, args.seeds, args.bootstrap)

if __name__ == "__main__":
    main()
