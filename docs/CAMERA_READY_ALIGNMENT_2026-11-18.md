# Camera-ready manuscript ↔ repository alignment (18 November 2026)

**Status:** targeted documentary cross-check, not a fresh end-to-end experimental rerun. Repository remains **private** pending formal publication and author approval.

## Manuscript snapshot

- **Accepted paper:** *Quantum-Inspired Bloch Feature Fusion for Full-Polarimetric SAR Ship Candidate Verification* (SEQUENCE 2026, Paper #67).
- **Authors:** Sakthi Prabhu Gunasekar and Prasanna Kumar Rangarajan.
- **Compared artifact:** user-provided `Token_QBloch_Fusion_Full_Pol_SAR_CameraReady(8).pdf` (19 pages, 18 November 2026). The submitted PDF is **not** redistributed from this repository.
- **Bibliography:** publisher DOI/proceedings URL not yet confirmed. Do not invent or preemptively add an identifier to `CITATION.cff`.

## Cross-checked claims

| Item | Camera-ready manuscript | Repository evidence |
|:--|:--|:--|
| Stage 1 | PauliYOLOv8n proposals, separate from verifier | `docs/ARCHITECTURE.md`; `configs/input_provenance.json` |
| Stage 2 input | 64×64 nine-channel candidate chip; 6×6 = 36 tokens | `docs/ARCHITECTURE.md`; archived EXP37 notebook |
| Feature fusion | 8D handcrafted PolSAR + 12D simulated Bloch–Pauli features = 20D per token | `README.md`; `docs/ARCHITECTURE.md` |
| Simulated branch | Three qubits, two trainable `Rz–Ry–Rz` layers, CNOT ring after each layer | `docs/ARCHITECTURE.md` |
| Branch parameters | QBloch 18; classical projection 100 | `docs/ARCHITECTURE.md` |
| Total verifier parameters | Token–QBloch 10,547; Token–Control 10,629 | `docs/ARCHITECTURE.md`; `README.md` |
| Main 10-seed AP | 0.6425 ± 0.0128 versus 0.6316 ± 0.0094 | `README.md`; archived summary |
| Main 10-seed AUC | 0.8242 ± 0.0070 versus 0.8141 ± 0.0071 | `README.md`; checkpoint replay record |
| Main 10-seed F1 | 0.6652 ± 0.0131 versus 0.6530 ± 0.0145 | `README.md`; archived summary |
| Main paired-seed AUC gain | +0.0101, Wilcoxon p ≈ 0.006 | `README.md`; `results/verification/checkpoint_replay_2026-11-15.json` |
| Candidate-level paired bootstrap | +0.0070, 95% CI [+0.0006, +0.0138] | `README.md`; archived analyses |
| Validation candidate cache | 1,074 candidates (355 positive, 719 negative) | `configs/input_provenance.json`; checkpoint replay record |

**Interpretation:** the paired-seed AUC comparison and candidate-level paired bootstrap are distinct estimands. Do not substitute either value for the other. The no-entanglement ablation does not establish a significant independent CNOT-ring AUC benefit. All QBloch computations are classical simulations, not quantum-hardware experiments.

## What was, and was not, verified here

- Verified the *reported text and tabulated values* above against the supplied camera-ready PDF and the checked-in README/architecture/provenance/replay records.
- Existing checkpoint replay validates inference from **20 saved primary checkpoints** on the archived validation cache, **not** regeneration from raw FPSD images.
- This documentary check did **not** re-run full detector training, regenerate candidate proposals, repeat all model trainings, perform a complete history-wide secret scan, or adjudicate third-party redistribution rights.
- The original FPSD dataset, PauliYOLOv8n weights, validation-cache binaries and other restricted assets must remain excluded unless lawful redistribution rights are established.

## Publication/release gate

1. The manuscript's *Data and Code Availability* section points to `https://github.com/SakthiGs/polsar-token-qbloch` and says implementation/notebooks/scripts are available. **Readers outside the owner account cannot access that link while the repo is private.** Arrange author-approved public visibility by the time the article is published; do not claim current public availability.
2. Confirm all source-code ownership, coauthor consent, relevant upstream licenses (including Ultralytics obligations) and complete git-history secret/PII review. A public repo without a `LICENSE` file does **not** automatically grant reuse rights.
3. Confirm final published title, proceedings citation, DOI and publisher URL before updating `CITATION.cff` or cutting a versioned release.
4. Do not describe the repo as fully raw-FPSD reproducible until the remaining steps in `docs/RELEASE_READINESS.md` are completed.

**Decision for 18 November 2026:** update documentation on the private repository; do not change GitHub visibility or license, and do not upload data, weights or the manuscript PDF.
