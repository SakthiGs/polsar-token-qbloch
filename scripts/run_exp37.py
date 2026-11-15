#!/usr/bin/env python3
"""Run the canonical EXP37 notebook with explicitly selected synthetic or FPSD inputs.

The FPSD path requires a separately obtained dataset, labels, and YOLO weights.
"""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb"
REQUIRED_FULL = [
    "POLSAR_FPSD_ROOT", "POLSAR_YOLO_BEST", "POLSAR_TRAIN_IMAGE_DIR",
    "POLSAR_TRAIN_TIF_DIR", "POLSAR_TRAIN_ANN", "POLSAR_VAL_IMAGE_DIR",
    "POLSAR_VAL_TIF_DIR", "POLSAR_VAL_ANN",
]

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["synthetic", "fpsd"], default="synthetic")
    parser.add_argument("--timeout", type=int, default=900, help="Seconds allowed per cell")
    parser.add_argument("--output-root", type=Path, default=ROOT / "outputs")
    args = parser.parse_args(argv)
    if args.mode == "fpsd":
        missing = [name for name in REQUIRED_FULL if not os.getenv(name)]
        if missing:
            parser.error("FPSD mode requires: " + ", ".join(missing))
        for name in REQUIRED_FULL:
            if not Path(os.environ[name]).expanduser().exists():
                parser.error(f"{name} does not exist: {os.environ[name]}")
    import nbformat
    from nbclient import NotebookClient
    args.output_root.mkdir(parents=True, exist_ok=True)
    os.environ["POLSAR_REPO_ROOT"] = str(ROOT)
    os.environ["POLSAR_OUTPUT_ROOT"] = str(args.output_root.resolve())
    os.environ["POLSAR_DRY_RUN"] = "true" if args.mode == "synthetic" else "false"
    os.environ["POLSAR_RUN_EXPERIMENT"] = "true"
    nb = nbformat.read(NOTEBOOK, as_version=4)
    NotebookClient(
        nb, timeout=args.timeout, kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}},
        allow_errors=False,
    ).execute()
    report = args.output_root / ("notebook_run_" + args.mode + ".json")
    report.write_text(json.dumps({
        "mode": args.mode,
        "notebook": NOTEBOOK.name,
        "status": "completed",
        "cells": len(nb.cells),
    }, indent=2) + "\n")
    print("PASS:", args.mode, "notebook execution. Report:", report)
    if args.mode == "synthetic":
        print("NOTE: synthetic data only; does not verify published FPSD results.")

if __name__ == "__main__":
    main()
