# Token–QBloch Fusion for PolSAR Ship Candidate Verification

**SEQUENCE 2026 Paper #67 | Research artifact | Private until publication and release approval**

**Authors:** Sakthi Prabhu Gunasekar; Prasanna Kumar Rangarajan

This repository contains the experiment implementation, archived statistical results, tests, and checkpoint-replay tools for a **second-stage PolSAR ship-candidate verifier**. It is **not** a claim of quantum hardware execution, quantum computational advantage, or improved end-to-end ship detector mAP.

## Main architecture

The following diagram follows the actual \`EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb\` implementation. **QBloch is quantum-inspired and simulated on classical hardware.**

\`\`\`mermaid
flowchart TD
    A["FPSD PolSAR image<br/>nine real-valued C9 channels"] --> B["Stage 1: PauliYOLOv8n<br/>ship candidate proposals"]
    B --> C["Candidate-centered chip<br/>64 × 64 pixels"]
    C --> D["6 × 6 local grid<br/>36 patches per candidate"]

    D --> E["Classical stream<br/>8 features per patch:<br/>log span, 3 coherence magnitudes,<br/>3 relative phases, entropy"]
    D --> F["Polarimetric stream<br/>normalized 3 × 3 complex<br/>coherency matrix per patch"]

    F --> G["Three polarization-pair states<br/>(0,1), (0,2), (1,2)<br/>Bloch / 2 × 2 density matrices"]
    G --> H["Three-qubit product state<br/>classically simulated 8 × 8 density matrix"]
    H --> I["2 trainable circuit layers<br/>Rz–Ry–Rz on each qubit<br/>CNOT ring 0→1→2→0 after each layer"]
    I --> J["12 Pauli expectation values<br/>9 single-qubit + 3 ZZ pair terms<br/>12 features per patch"]

    E --> K["Concatenate per patch<br/>8D classical + 12D QBloch = 20D"]
    J --> K

    K --> L["Linear projection 20D → 32D<br/>CLS token + position embedding"]
    L --> M["One transformer encoder layer<br/>4 attention heads"]
    M --> N["Binary candidate verifier<br/>Ship / false alarm score"]
\`\`\`

**What is fused:** 36 local *classical* 8D tokens are concatenated **per patch** with 36 *quantum-inspired* 12D Pauli-readout vectors. The final transformer learns a candidate-level decision. The CNOT ring does **not** operate on quantum hardware.

**What is novel in the experiment:** the specifically constructed polarization-pair Bloch feature branch, its fusion with local PolSAR tokens, and the matched classical-control comparison—not the invention of a new quantum gate. The entanglement ablation did not establish a statistically reliable **AUC** benefit for the CNOT ring.

See [architecture and parameter-accounting notes](docs/ARCHITECTURE.md).

## Circuit details and verified parameter accounting

- Three polarization-pair density matrices form an **8 × 8** product state.
- Two simulated trainable layers; each layer has three qubits × three angles in **Rz–Ry–Rz**, followed by CNOTs **0→1, 1→2, 2→0**.
- **18 trainable QBloch parameters = 2 layers × 3 qubits × 3 angles.**
- The classical control is a **9 → 4 → 12** MLP, with **100** trainable parameters.
- Full verifier: **10,547** (Token–QBloch) versus **10,629** (Token–Control): the difference **82** matches **100 − 18**.
- A previous manuscript draft incorrectly stated **12** QBloch branch parameters; the camera-ready text and figure should use **18**.

## Results and evidence level

| Evidence | Token–QBloch | Matched classical control |
|:--|--:|--:|
| Archived AUC, 10 seeds (42–51) | **0.8242 ± 0.0070** | 0.8141 ± 0.0071 |
| Archived AP, 10 seeds | **0.6425 ± 0.0128** | 0.6316 ± 0.0094 |
| Archived F1, 10 seeds | **0.6652 ± 0.0131** | 0.6530 ± 0.0145 |
| Trainable parameters, entire verifier | **10,547** | **10,629** |

The archived seed-paired AUC gain is **+0.0101** (two-sided Wilcoxon **p ≈ 0.006**). The separately reported candidate-level paired bootstrap gain is approximately **+0.0070**, 95% CI **[+0.0006, +0.0138]**. These are different analysis units and should not be conflated.

**Checkpoint replay:** An independent CPU evaluation of **20 saved primary-model checkpoints** on the archived **1,074-candidate** validation cache reproduced mean AUCs **0.8241889 vs 0.8140896**, gain **0.0100993** (Wilcoxon **p = 0.005859375**). This validates archived checkpoint inference, **not** the generation of those candidate chips from the original images. See [evidence record](results/verification/checkpoint_replay_2026-11-15.json).

## Quick start — reproducible without restricted data

Use Python 3.11 or a compatible supported environment:

\`\`\`bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify_archived_results.py
python -m unittest discover -s tests -v
python scripts/run_exp37.py --mode synthetic --timeout 300
\`\`\`

The last command runs on **generated synthetic test inputs** only. It must not be presented as reproduction of FPSD scores. For Windows, activate the environment using \`.venv\Scripts\activate\`.

For lawful access to FPSD, original PauliYOLO weights and the full experiment path, see [reproducing the experiment](docs/REPRODUCING_EXPERIMENT.md) and [data access](docs/DATA_ACCESS.md). No dataset, cached features, or model weights are distributed here.

## Repository map

| Directory | Purpose |
|:--|:--|
| [notebooks/](notebooks/) | Two portable original EXP37 notebooks (no saved cell outputs) |
| [scripts/](scripts/) | Synthetic runner, archived table checks, checkpoint and prediction replay |
| [tests/](tests/) | Scientific unit tests, candidate-cache alignment, portable notebook tests |
| [results/summary/](results/summary/) | Eight variants × ten seeds and statistical summaries |
| [results/verification/](results/verification/) | Primary-model checkpoint replay evidence |
| [docs/](docs/) | Architecture, data provenance, licensing and reproducibility boundaries |
| [.github/workflows/](.github/workflows/) | Automated scientific and synthetic execution checks |

## Public release after publication

**Current status: private pre-publication research archive.** Passing GitHub Actions does not remove external-data, historical environment, rights or coauthor-licensing requirements. The [release-readiness checklist](docs/RELEASE_READINESS.md) explicitly separates verified activities from remaining blockers.

- Do not upload third-party FPSD imagery, labels, raw feature caches or pretrained YOLO weights without explicit permission and compatible licenses.
- Ultralytics software and default models use **AGPL-3.0** unless separately licensed; derivative-work compliance needs author review. See [licensing assessment](docs/LICENSE_AND_RIGHTS.md).
- The original 2026 training environment is **not** established by a later \`pip freeze\` file.
- Add the publisher-issued **DOI**, bibliographic details and versioned release tag to [CITATION.cff](CITATION.cff) only after the paper is published.

No software \`LICENSE\` is present yet: the repository is **not currently offered as open-source licensed code**. Public visibility is a separate action that requires explicit author approval; none is being taken here.
