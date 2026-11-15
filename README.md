# Token–QBloch: PolSAR ship candidate verification

**Status:** Private, research staging repository. **Not yet an independently reproduced public release.**

Supporting materials for SEQUENCE 2026 Paper #67, *Quantum-Inspired Bloch Feature Fusion for Full-Polarimetric SAR Ship Candidate Verification* (S. P. Gunasekar and P. K. Rangarajan).

## Scientific scope

A two-stage framework uses a detector to propose ship candidates, followed by a lightweight verifier that consumes image and full-polarimetric SAR features. Comparisons include a token-only TinyViT baseline, a classical fusion control, a quantum-inspired Bloch feature fusion, and ablations.

The *quantum-inspired* model is a **classical simulation**, not a claim of a quantum speedup or quantum-hardware execution.

## Important camera-ready correction

The experimental implementation uses two layers of a three-qubit, three-trainable-rotation-per-qubit ansatz: **2 × 3 × 3 = 18** trainable branch angles. The original manuscript incorrectly stated **12** for that branch. With 18 (not 12), the parameter accounting is consistent:

| Model | Branch trainable parameters | Total trainable parameters |
|---|---:|---:|
| Token–QBloch Fusion | 18 | 10,547 |
| Token–Control Fusion | 100 | 10,629 |

The model totals differ by **82**, as do the branch counts. The description and circuit diagram require camera-ready corrections. See [architecture notes](docs/ARCHITECTURE_CORRECTIONS.md).

## Archived results

CSV files in [results/summary](results/summary/) are source records from the EXP37 experiment folder, including a ten-seed grid (seeds 42–51) and paired/bootstrap analyses.

Key archived ten-seed results:
- Token–QBloch Fusion: AP 0.6425 ± 0.0128; AUC 0.8242 ± 0.0070; F1 0.6652 ± 0.0131.
- Classical fusion control: AUC 0.8141 ± 0.0071.
- Paired AUC difference: +0.0101 ± 0.0072, Wilcoxon two-sided p = 0.006.
- Candidate-level paired bootstrap AUC gain: +0.0070, 95% CI [+0.0006, +0.0138] (2,000 resamples).

These figures are **archived analysis outputs**, not evidence that the entire pipeline has been rerun here from raw data.

## Repository contents

- `results/summary/`: archived, tabular experiment outputs from the Drive EXP37 folder.
- `configs/config.example.json`: sanitized example settings, not a frozen exact reproduction config.
- `docs/`: corrections, provenance, and release-gating requirements.
- `notebooks/`: staging notes; cleaned notebooks are **not committed in this initial repository import**.

## Reproducibility boundaries

The original notebooks use Google Colab/Drive paths, cached candidate inputs and pretrained detector weights. Before claiming independent reproduction, we must provide code, environment locks, provenance/hashes, data access instructions, prediction artifacts and full re-execution checks. See [release readiness](docs/RELEASE_READINESS.md).

## Data and license

**Do not upload raw FPSD data, detector weights, patient or personal data, credentials, or private Drive links.** Verify dataset redistribution and third-party library/weight licensing before publishing a public release. No open-source license is granted by this repository at this stage.

## Manuscript

The camera-ready revision must be checked against both SEQUENCE 2026 technical and formatting reports before proceeding to the publisher.
