# Notebook portability and execution

The two EXP37 source notebooks were taken from the author's Drive, cleaned of cell outputs/temporary diagnostics, and revised to remove machine-specific paths. The model equations, training seeds, model-variant registry, and statistical analyses were left in place.

## Safe synthetic smoke test

Install `requirements.txt`. Start Jupyter in repository root (`jupyter lab`) and open either file under `notebooks/`. With no environment variables set, `POLSAR_DRY_RUN=true` and `POLSAR_RUN_EXPERIMENT=true`, running all cells generates synthetic data and tests model forward passes, metrics and logging without real FPSD data.

Both notebooks passed that synthetic "Run All" test in a CPU environment on 2026-11-15. This is **not** a reproduction of the published FPSD numbers.

## Full FPSD execution

Install `requirements-full.txt`; provide access to the FPSD source data and existing YOLO detector weight. Set:
- `POLSAR_REPO_ROOT` to the repository directory if running Jupyter elsewhere.
- `POLSAR_FPSD_ROOT` to the extracted FPSD dataset root.
- `POLSAR_OUTPUT_ROOT` to a writable output directory.
- `POLSAR_YOLO_BEST` to the exact archived detector weight.
- `POLSAR_EXP31_RUN_FOLDER` optionally to the original detector-run directory.
- `POLSAR_TRAIN_IMAGE_DIR`, `POLSAR_TRAIN_TIF_DIR`, `POLSAR_TRAIN_ANN`, and corresponding `POLSAR_VAL_*` values if automatic subfolder discovery is insufficient.
- `POLSAR_DRY_RUN=false` and `POLSAR_RUN_EXPERIMENT=true` explicitly for real training.

The notebooks no longer automatically mount Google Drive or pip-install packages. They require **both** train and validation inputs and refuse the original validation-to-training fallback to guard against sample leakage. They also will not silently select a recent, unrelated YOLO checkpoint.

## Known remaining risks

The historical cache key does not encode all input/weight provenance. Clear caches if dataset splits or detector checkpoints change, then record the exact hashes. The candidate-level bootstrap does not support an image-level claim. The full raw-data workflow and environment lockfile need external validation with the authorized data and weight files.

No raw FPSD data or pretrained detector is distributed here.
