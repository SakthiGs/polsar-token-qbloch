#!/usr/bin/env python3
"""Verify archived EXP37 tables internally; does NOT reproduce from raw FPSD."""
from pathlib import Path
import csv
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "summary"

def read_csv(filename):
    with (DATA / filename).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def check():
    grid = read_csv("grid_per_seed_metrics.csv")
    require(len(grid) == 80, "Expected eight models x ten seeds")
    models = {r["model"] for r in grid}
    seeds = sorted({int(r["seed"]) for r in grid})
    require(len(models) == 8, "Expected eight distinct model variants")
    require(seeds == list(range(42, 52)), "Unexpected seed set")
    require(len({(r["model"], r["seed"]) for r in grid}) == 80, "Duplicate model-seed rows")
    table = {r["model"]: r for r in read_csv("tableA_verifier_comparison.csv")}
    for model, key, col in [
        ("Token_Arch2Quantum_Fusion", "avg_precision", "AP"),
        ("Token_Arch2Quantum_Fusion", "roc_auc", "AUC"),
        ("Token_Arch2Quantum_Fusion", "f1", "F1"),
        ("Token_Arch2Control_Fusion", "roc_auc", "AUC")
    ]:
        vals = [float(r[key]) for r in grid if r["model"] == model]
        require(len(vals) == 10, "Missing seed values")
        m, sd = map(float, table[model][col].split("±"))
        require(abs(mean(vals)-m) < 0.00006, "Mean mismatch: "+model+" "+col)
        require(abs(stdev(vals)-sd) < 0.00006, "SD mismatch: "+model+" "+col)
    require(int(table["Token_Arch2Quantum_Fusion"]["params"]) == 10547, "Quantum params mismatch")
    require(int(table["Token_Arch2Control_Fusion"]["params"]) == 10629, "Control params mismatch")
    paired=read_csv("tableB_auc_significance.csv")
    comp=next(r for r in paired if r["comparison"]=="Token_Arch2Quantum_Fusion - Token_Arch2Control_Fusion")
    require(comp["pos"]=="9/10", "Unexpected positive-seed count")
    require(abs(float(comp["wilcoxon_2s"])-0.006)<0.0005, "Wilcoxon p mismatch")
    boot=read_csv("tableC2_paired_bootstrap_delta.csv")
    main=next(r for r in boot if r["comparison"]=="Token_Arch2Quantum_Fusion - Token_Arch2Control_Fusion")
    require(main["level"]=="candidate" and int(main["b_boot"])==2000, "Bootstrap level/count mismatch")
    require(float(main["ci_lo"])>0, "Unexpected CI lower bound")
    print("PASS: archived CSVs internally consistent (8 models, 10 seeds, metrics, parameters, paired tests).")
    print("NOTE: not an FPSD raw-data rerun.")

if __name__ == "__main__":
    check()
