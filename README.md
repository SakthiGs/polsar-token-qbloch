# Token–QBloch Fusion for PolSAR Ship Candidate Verification

**SEQUENCE 2026 Paper #67 — research artifact, currently PRIVATE.**

Authors: Sakthi Prabhu Gunasekar and Prasanna Kumar Rangarajan.

This is a two-stage PolSAR ship-candidate **verification** system, not a claim of quantum hardware execution or end-to-end ship detection mAP improvement.

## Pipeline

1. A PauliYOLOv8n detector proposes ship candidate boxes (confidence 0.001, NMS IoU 0.65, maximum 300 per image).
2. Each candidate yields a 64×64 pixel chip of nine real-valued covariance/coherency channels: C11, Re/Im C12, Re/Im C13, C22, Re/Im C23, C33.
3. A 6×6 grid yields 36 patches. Each patch has an 8D classical feature token (log span, three coherence magnitudes, three phases, entropy) and a normalized 3×3 complex matrix.
4. Three polarization pairs (0,1), (0,2), (1,2) map into Bloch states. A simulated three-qubit product density matrix passes through two layers of Rz–Ry–Rz rotations plus a three-CNOT ring after **each** layer. Twelve Pauli readouts supply the quantum-inspired features.
5. The 8D classical and 12D quantum-inspired features are concatenated, projected into a 32D four-head transformer verifier, and classified as ship or false alarm.

The quantum-inspired branch has **18** trainable angles; the classical 9→4→12 MLP control has **100** parameters. Corresponding total verifier parameters are **10,547 versus 10,629**, both differences 82.

## Results

The original archive holds eight models × ten seeds (42–51).
- QBloch fusion AP **0.6425 ± 0.0128**, AUC **0.8242 ± 0.0070**, F1 **0.6652 ± 0.0131**.
- Classical fusion AUC **0.8141 ± 0.0071**.
- Seed-paired AUC gain **+0.0101**, Wilcoxon two-sided **p=0.006**.
- Candidate-level paired bootstrap AUC improvement ~+0.0070, 95% CI [+0.0006,+0.0138].

**Independent checkpoint-level CPU replay:** Twenty original checkpoints, ten seeds per primary model, reproduced AUC **0.8241889 vs 0.8140896**, gain **+0.0100993**, Wilcoxon **p=0.005859375** on the archived 1,074-candidate FPSD validation cache. See [replay proof](results/verification/checkpoint_replay_2026-11-15.json). Small per-seed CPU differences remain. **This is not an independent rerun starting from raw FPSD images.**

## Quick start

```
python -m pip install -r requirements.txt
python scripts/verify_archived_results.py
python -m unittest discover -s tests -v
python scripts/run_exp37.py --mode synthetic --timeout 300
```

The default executes the canonical notebook on **synthetic data**, not FPSD. For optional checkpoint replay, prediction-level bootstrap and full raw-data prerequisites, see [reproduction guide](docs/REPRODUCING_EXPERIMENT.md).

## Contents

- `notebooks/` — full EXP37 notebooks; original model/experiment code with outputs and hard-coded Drive paths removed
- `scripts/` — archival table checks, CLI notebook execution, checkpoint and prediction replays
- `tests/` — implemented quantum circuit, model parameter, prediction, and notebook portability tests
- `results/summary/` — original ten-seed results and statistical summaries
- `results/verification/` — checkpoint replay evidence
- `docs/` — source data, experiment recreation, rights, limitations and release gate
- `.github/workflows/` — automated scientific tests and synthetic-run smoke test

## Open-science status

The repository intentionally excludes raw FPSD imagery, labels, cached features and trained detector/verifier weights. The [original FPSD repository](https://github.com/Yanhui-Struggle/FPSD) is public, but its data redistribution rights still require verification. Ultralytics YOLO has distinct AGPL-3.0/enterprise terms. **No software license is granted in this repository yet.** Public visibility and raw-data reproducibility are separate decisions; see [release gate](docs/RELEASE_READINESS.md).
