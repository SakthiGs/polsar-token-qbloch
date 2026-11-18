# EXP37 notebooks (staged)

- `EXP37_FINAL_CLEAN_20260615_TOKEN_QBLOCH_FIDELITY.ipynb`: token baseline, quantum/classical fusion, detector-confidence helper, synthetic test.
- `EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb`: entanglement ablations (M1), bootstrap confidence intervals (M2) and candidate-level paired bootstrap (M2b).

Changes from Drive originals: removed stored cell outputs, replaced hard-coded Colab/Drive paths with `POLSAR_*` settings, defaulted to safe synthetic run, removed stale path diagnostics/forced installs, disabled data-leaking validation-to-training fallback, and made detector-only helper optional in dry-run.

**Verification boundary (checked 18 November 2026):** Both notebooks completed synthetic Run All with `NOTEBOOK_SELF_TEST` passing in the prior 15 November CPU check. Both stored notebooks have a Python 3 kernelspec and no retained execution outputs; the canonical M1/M2 notebook has 28 cells (22 code), while the earlier FINAL_CLEAN notebook has 29 cells (26 code). The current GitHub Actions workflow runs the **canonical M1/M2 notebook only**; a new, independent execution of both notebooks was **not** performed during the documentation audit. End-to-end FPSD ingestion, detector inference, training and complete paper-score reproduction are **not independently verified**. See [portability and execution](../docs/PORTABILITY.md).
