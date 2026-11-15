# Release-readiness audit — 15 November 2026

**Current GitHub visibility: PRIVATE. No automatic public visibility change approved.**

## Verified in this repository

- [x] Two portable original EXP37 notebooks, outputs stripped, original scientific code retained.
- [x] Archived table integrity: eight variants × seeds 42–51.
- [x] Correct branch counts (18 vs 100) and total parameters (10,547 vs 10,629).
- [x] Scientific unit tests for unitarity, Pauli-Y Bloch convention, model counts and finite output.
- [x] Local end-to-end synthetic notebook run.
- [x] A checkpoint-level CPU replay of 20 archived QBloch/control models on the original held-out cache: quantum AUC ~0.824189, classical AUC ~0.814090, paired p ~0.005859.
- [x] Candidate-cache provenance now incorporates detector/annotation identity, and cache retains aligned candidate image metadata.
- [x] Prediction-level paired bootstrap can be recomputed from saved per-candidate NPZs without raw FPSD.
- [x] Raw imagery and model weight binaries excluded.

## Still outstanding for a *complete public, independently reproducible FPSD paper artifact*

- [ ] Independently process original FPSD TIF+JPG source files and train/evaluate the historical PauliYOLOv8n detector.
- [ ] Independently rebuild candidate caches, verify data split/image overlap, train all 80 checkpoints and match published metrics.
- [ ] Establish exact package versions from the original June 2026 environment and full source-image checksums.
- [ ] Confirm FPSD data redistribution rights and Ultralytics software/weight licensing compatibility.
- [ ] Choose an author-approved repository LICENSE.
- [ ] Inspect entire repository history, not only its latest tree, for secrets/restricted third-party data.

**Allowed description:** research code with verified checkpoint-level replication and executable synthetic testing.

**Not yet supported:** independently reproduced from original raw FPSD; licensed unrestricted public release; quantum hardware advantage; improved end-to-end detector mAP.
