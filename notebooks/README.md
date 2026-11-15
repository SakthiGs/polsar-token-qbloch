# EXP37 notebooks (staged)

- `EXP37_FINAL_CLEAN_20260615_TOKEN_QBLOCH_FIDELITY.ipynb`: token baseline, quantum/classical fusion, detector-confidence helper, synthetic test.
- `EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb`: entanglement ablations (M1), bootstrap confidence intervals (M2) and candidate-level paired bootstrap (M2b).

Changes from Drive originals: removed stored cell outputs, replaced hard-coded Colab/Drive paths with `POLSAR_*` settings, defaulted to safe synthetic run, removed stale path diagnostics/forced installs, disabled data-leaking validation-to-training fallback, and made detector-only helper optional in dry-run.

**Verification:** both notebooks completed a synthetic run-all with `NOTEBOOK_SELF_TEST` passing. End-to-end FPSD data execution is not yet independently verified. See `docs/PORTABILITY.md`.
