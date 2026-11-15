# Token–QBloch Fusion for PolSAR Ship Candidate Verification

**Research status:** Private staging repository supporting SEQUENCE 2026 Paper #67. Portable synthetic notebook smoke tests pass; a clean independent reproduction on FPSD has **not** yet been performed.

## Research

Two-stage ship candidate detection and verification using PolSAR coherency-derived features, TinyViT tokens and a quantum-inspired three-qubit Bloch representation. The latter runs on a classical simulator, not on quantum hardware.

**Camera-ready correction:** Two layers × three qubits × three trainable rotations (Rz–Ry–Rz) per qubit = **18** quantum-branch parameters, not 12. Thus the Token–QBloch verifier has **10,547** parameters and its classical fusion control **10,629**; the difference **82** matches the branches (100−18). The diagram and text in the paper also need to reflect the implemented CNOT sequence.

## Archived EXP37 results

`results/summary/` contains ten-seed (42–51) metrics and analysis tables from the archived June 19 EXP37 run. Token–QBloch AP **0.6425 ± 0.0128**, AUC **0.8242 ± 0.0070**, F1 **0.6652 ± 0.0131**. Classical fusion AUC **0.8141 ± 0.0071**. Paired seed-level AUC gain **+0.0101**, Wilcoxon two-sided p **0.006**. Candidate-level paired bootstrap gain **+0.0070** with 95% CI **[+0.0006,+0.0138]**. Image-level bootstrap has **not** been established.

These CSVs are an audited result archive, not freshly regenerated measurements.

## Files

- `notebooks/`: two sanitized EXP37 notebooks with environment-driven paths, no stored outputs, and safe synthetic default.
- `results/summary/`: six archived CSV tables.
- `configs/config.example.json`: illustrative configuration (not an original run manifest).
- `docs/`: architecture correction, portability, statistical provenance and release checklist.
- `scripts/verify_archived_results.py`, `tests/`: internal data-consistency and portability checks.

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/verify_archived_results.py
python -m unittest discover -s tests -v
jupyter lab
```

Run Jupyter from the repository root; **Run All** in either notebook uses synthetic data by default. Full FPSD requires your own authorized dataset, pretrained detector, verified split mapping and `POLSAR_*` environment variables. See [portability guide](docs/PORTABILITY.md).

## Boundaries and licensing

No dataset imagery, trained checkpoints, signed forms, or credentials are included. External FPSD data and YOLO/Ultralytics weights and redistribution require a rights assessment. **No open-source license has been selected yet.** Keep the repo private until full-path and rights audits are complete. Notebooks retain the original model/statistics logic but *were not independently rerun on raw FPSD* here.

**Manuscript:** SEQUENCE 2026 Paper #67, Sakthi Prabhu Gunasekar and Prasanna Kumar Rangarajan. Official DOI to be added only when publisher issues one.
