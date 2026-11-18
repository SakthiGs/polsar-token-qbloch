# Release-readiness audit — updated 18 November 2026

**Visibility: PRIVATE. User intends to release only after the paper is formally published; no visibility change is authorized now.**

## Verified in the current repository

- [x] Main architecture diagram and exact feature dimensions sourced from the implemented notebook.
- [x] Two output-cleaned, portable original EXP37 notebooks.
- [x] Archived metrics for eight model variants × seeds 42–51 and statistical integrity checks.
- [x] QBloch branch 18 parameters; classical branch 100; total models 10,547 and 10,629.
- [x] Scientific unit tests for unitarity, Bloch Pauli-Y sign, trainable parameters and finite model output.
- [x] Both notebooks' synthetic Run All checks previously passed (15 November 2026); the repository workflow executes the canonical M1/M2 synthetic notebook. No new Actions status or fresh FPSD rerun is asserted for the 18 November documentation commits.
- [x] Checkpoint-level CPU replay of 20 primary-model weights against the archived 1,074-candidate validation cache; main rounded AUCs reproduced.
- [x] Candidate-cache invalidation includes detector/annotation fingerprints and aligned metadata; bootstrapping from per-candidate predictions is supported when assets are supplied.
- [x] No raw imagery, feature-cache binary or weights in any of the 11 reachable main-history Git trees inspected.
- [x] Sources and limits for FPSD and Ultralytics licensing documented.
- [x] Later `pip_freeze.txt` rejected as falsely representing the original June 2026 environment.
- [x] Original archived PauliYOLOv8n `best.pt` located and hashed; original stage-one training settings inventoried without uploading weights.
- [x] Original train/val COCO TIFF annotations hashed and validated for disjoint filenames (768 vs 85 images); split-local COCO numeric IDs overlap and are not globally unique.

## Blocking a claim of complete, independently reproduced raw-data research

- [ ] Reconstruct the full original FPSD source-image pipeline (JPG/TIF + annotations) in a fresh controlled environment.
- [ ] Independently reproduce PauliYOLOv8n training/proposals from the original image inputs. The archived `best.pt` checkpoint has already been located and SHA-256 hashed, but fresh detector training has **not** been reproduced.
- [ ] Regenerate candidate caches; establish train/val image-level disjointness and verify the full 80-checkpoint experiment from original inputs.
- [ ] Recover the exact original June 2026 Python/package/CUDA environment and full source-image/weight hashes, if those records exist.

## Blocking a *legally cleared public software release*

- [ ] Establish author/coauthor permission to release the source and select a license compatible with all third-party components; **no default license is imposed by ChatGPT**.
- [ ] Verify FPSD rights for every redistributed artifact; keep raw data excluded unless permissions are explicit.
- [ ] Review Ultralytics AGPL obligations and detector weight distribution before choosing public repository rights.
- [ ] Run full-history secrets/PII scan across all refs and manually review flagged content.
- [ ] Await confirmed publisher metadata and DOI, then update `CITATION.cff` and create a reviewed release tag.
- [ ] Obtain explicit authorization before changing GitHub visibility from Private to Public.
- [ ] Reconcile the camera-ready *Data and Code Availability* wording (which links to this GitHub repository) with actual public access at the time of formal proceedings publication; see [camera-ready alignment](CAMERA_READY_ALIGNMENT_2026-11-18.md).

## Distinguish two release levels

A **code-only public research artifact** can be suitable if it has a legally compatible source license, clean history, citation and honest limits. It need not reproduce the inaccessible raw FPSD data automatically. A **fully reproducible from raw FPSD** release additionally needs the historical data/weights/split processing and a controlled full rerun.

**Allowed claim today:** archived summary metrics, executable notebooks on synthetic inputs, and independently replayed 20 checkpoint inferences on the original validation cache.

**Not supported today:** exact June training environment, full raw-image reproduction, reproducible detector training, quantum hardware/advantage or demonstrated end-to-end detector mAP improvement.
