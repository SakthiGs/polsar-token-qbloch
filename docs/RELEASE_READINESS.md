# Release readiness — private research staging

## Verified

- [x] Repository remains private.
- [x] Eight registered model variants × ten seeds have archived EXP37 per-seed result rows.
- [x] Main AP/AUC/F1 summaries, parameter totals, seed-level Wilcoxon and candidate-level bootstrap CSVs are internally consistent.
- [x] Corrected branch accounting documented: 18 quantum angles versus 100 classical branch parameters.
- [x] Both notebooks stripped of saved outputs and user-specific absolute paths.
- [x] Both notebooks passed synthetic CPU Run All and their built-in self-tests (2026-11-15).
- [x] A static notebook integrity test and an archived-CSV consistency check were prepared.

## Still needed before public release

- [ ] Reproduce end-to-end detector generation and verifier evaluation with a clean environment using exact FPSD split, detector weights and candidate cache.
- [ ] Verify model weight/checkpoint and dataset hashes and record original June 2026 environment package versions.
- [ ] Export and validate per-candidate predictions and IDs; assess image-level bootstrap if making that claim.
- [ ] Verify no train/validation sample leakage and check cache invalidation on different weights/datasets.
- [ ] Audit FPSD redistribution rights; audit Ultralytics/third-party code and weights licenses.
- [ ] Audit paper/source and bibliography against camera-ready corrections and final publisher approval.
- [ ] Decide a code license based on provenance; do not assume original notebook dependencies are redistributable.

Do **not** present the synthetic smoke test as independent validation of results on FPSD.
