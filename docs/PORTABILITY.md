# Notebook portability and execution

The two EXP37 source notebooks were taken from the author's Drive, cleaned of cell outputs/temporary diagnostics, and revised to remove machine-specific paths. The model equations, training seeds, model-variant registry, and statistical analyses were left in place.

## Safe synthetic smoke test

Install `requirements.txt`. Start Jupyter in repository root (`jupyter lab`) and open either file under `notebooks/`. With no environment variables set, `POLSAR_DRY_RUN=true` and `POLSAR_RUN_EXPERIMENT=true`, running all cells generates synthetic data and tests model forward passes, metrics and logging without real FPSD data.

Both notebooks passed that synthetic "Run All" test in a CPU environment on 2026-11-15 according to the previous verification record. The two notebook files were inspected again on 2026-11-18: both remain JSON-valid, Python-3 notebooks without stored execution outputs. **No fresh Run All was performed in this documentation update.** The GitHub Actions job currently runs the canonical `EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb` using `scripts/run_exp37.py`; it does not independently run both notebooks on every push. These tests are **not** a reproduction of the published FPSD numbers.

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

The current candidate-cache key includes the detector SHA-256, annotation SHA-256, split parameters and directory-inventory identity, as documented in `docs/REPRODUCING_EXPERIMENT.md`. Directory inventories are **not** substitutes for complete image-file content hashes, and the original source-image pipeline has not been freshly rerun. Clear/rebuild caches when inputs change and record complete hashes. Candidate-level bootstrap does not establish image-level uncertainty. The full raw-data workflow and historical environment lockfile still need independent validation with authorized data and weights.

No raw FPSD data or pretrained detector is distributed here.
