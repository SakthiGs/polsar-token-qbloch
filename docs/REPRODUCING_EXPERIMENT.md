# Reproducing the SEQUENCE 2026 EXP37 result

## Verified levels

1. **Archived results:** eight model variants × ten seeds; numerical table consistency checked.
2. **Executable synthetic workflow:** the canonical notebook executes in a new kernel with generated data.
3. **Checkpoint-level replay:** ten QBloch and ten classical-control checkpoints on the archived 1,074-candidate held-out cache, reproducing the rounded main AUC comparison (proof in `results/verification/`).
4. **NOT reproduced independently:** full FPSD image ingestion, historical PauliYOLOv8n training/proposals, full 80-checkpoint training, original image-level split, and data/weight redistribution permissions.

## Installation and synthetic smoke

Use Python 3.11+ and a virtual environment. Run:

```
python -m pip install -r requirements.txt
python scripts/verify_archived_results.py
python -m unittest discover -s tests -v
python scripts/run_exp37.py --mode synthetic --timeout 300
```

This exercises only generated data.

## Original checkpoints and validation cache

With lawful access to the archived cache and checkpoint files:

```
python scripts/evaluate_checkpoints.py --cache /path/chips_val_9d3795bcf7.npz --checkpoints /path/ckpt --output outputs/checkpoint-replay
```

Expected approximate CPU result: QBloch AUC 0.8241889, classical AUC 0.8140896, mean delta 0.0100993, Wilcoxon p 0.005859375. Original cache SHA-256:

```
08f7f2b9e2136ede49e711b114d0757d126370f421299b553fd69c749d63e8d0
```

No cached PolSAR arrays or weights are included in GitHub.

## From raw FPSD (workflow supplied, independent execution pending)

Install `requirements-full.txt`. Obtain FPSD from its original source, check its use rights, and obtain the exact PauliYOLOv8n checkpoint from the study. Export paths to train/val JPG, nine-channel TIF and COCO annotations. Example:

```
export POLSAR_FPSD_ROOT=/path/FPSD
export POLSAR_OUTPUT_ROOT=/path/exp37-output
export POLSAR_YOLO_BEST=/path/weights/best.pt
export POLSAR_TRAIN_IMAGE_DIR=/path/FPSD/coco/train2017_jpg
export POLSAR_TRAIN_TIF_DIR=/path/FPSD/coco/train2017_tif
export POLSAR_TRAIN_ANN=/path/FPSD/coco/annotations/instances_train2017_tif.json
export POLSAR_VAL_IMAGE_DIR=/path/FPSD/coco/val2017_jpg
export POLSAR_VAL_TIF_DIR=/path/FPSD/coco/val2017_tif
export POLSAR_VAL_ANN=/path/FPSD/coco/annotations/instances_val2017_tif.json
python scripts/run_exp37.py --mode fpsd --timeout 3600
```

A run will refuse the old validation-to-training fallback. Cache keys include detector SHA-256, annotation SHA-256, split parameters and directory-inventory identity. Directory-inventory fingerprints alone do not replace full file checksums. Candidate image IDs are saved in the *post-extraction* feature order.

## Statistics from per-candidate predictions

After a complete real-data run saves prediction NPZs for the three primary models:

```
python scripts/reproduce_from_predictions.py --predictions /path/exp37-run/predictions --output outputs/recomputed --bootstrap 2000
```

Candidate- and image-cluster bootstrap are distinct, and image-cluster bootstrap requires aligned candidate-image IDs; the historical paper only established candidate-level bootstrap. See [readiness](RELEASE_READINESS.md).
