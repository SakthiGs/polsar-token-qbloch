# Private staging — release/readiness checklist

## Verified in the archived Drive outputs

- Ten seeds, 42–51, archived in a per-seed CSV for eight model variants.
- 80 checkpoint files were observed in a June 19 EXP37 run (eight variants × ten seeds).
- Main AP/AUC/F1, paired Wilcoxon p-value and bootstrap-delta CSVs match the quoted manuscript summary.
- Parameter-count discrepancy traced to 18 rather than 12 quantum-branch trainable angles.

These checks do **not** constitute an independent reproduction.

## Must complete before public release

- [ ] Upload and inspect original notebook sources. Remove outputs and unneeded cell outputs/metadata.
- [ ] Map exact paper tables/figures to frozen notebook cells, output files, and checkpoints.
- [ ] Remove or parameterize Colab/Drive-specific absolute paths.
- [ ] Capture exact package versions and setup instructions; test clean-environment execution.
- [ ] Document detector model, preprocessing, candidate cache provenance, data splits, seeds, and hashes.
- [ ] Validate reconstructed metrics from held-out predictions, not just mean result CSVs.
- [ ] Make retained candidate-level predictions and identifiers available when rights permit; document unavailable image IDs and corresponding bootstrap limitations.
- [ ] Do not represent candidate-level bootstrap intervals as image-level intervals.
- [ ] Validate signatures/checksums of exported datasets and checkpoints, where sharing is permitted.
- [ ] Check FPSD redistribution permissions and Ultralytics/YOLO and other third-party licensing.
- [ ] Scan source and notebook metadata for private paths, credentials, email addresses and tokens.
- [ ] Verify camera-ready manuscript, figures and signed administrative forms separately.

## Explicitly excluded from this initial commit

Raw FPSD data, checkpoints/weights, binary manuscript package, signed forms, and the original Colab notebooks. This initial private commit contains tracked analysis summaries and documentation. The original cleaned notebook files remain in the conversation's prepared starter package pending an authorized transfer path.
