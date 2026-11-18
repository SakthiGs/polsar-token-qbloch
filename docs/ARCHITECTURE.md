# Implemented EXP37 architecture — source-aligned technical note


## Manuscript Figures 1–3 — implementation-aligned architecture

The author-supplied updated manuscript \`Token-QBlochFusion.pdf\` (18 November 2026) describes three views of the same study. The diagrams below are **editable Mermaid equivalents** of their computational structure, not copies of the manuscript's graphical figure assets.

**Figure 3: entire two-stage pipeline, with experimentally evaluated boundary**

\`\`\`mermaid
flowchart TD
    A["FPSD PauliRGB image"] --> B["Stage 1: PauliYOLOv8n<br/>proposal boxes + detector confidence"]
    B --> C["Candidate boxes"]
    X["Co-registered full-polarimetric SAR<br/>nine real-valued C9 channels"] --> D
    C --> D["Extract 64 × 64 candidate-centered C9 chip"]
    D --> E["6 × 6 local regions = 36 tokens"]
    E --> F["Handcrafted PolSAR<br/>8D per token:<br/>log span, coherence, phase, entropy"]
    E --> G["Local normalized 3 × 3<br/>complex coherency matrix"]
    G --> H["Pairs (1,2), (1,3), (2,3)<br/>three Bloch-encoded 2 × 2 density matrices"]
    H --> I["Classically simulated<br/>three-qubit product state 8 × 8"]
    I --> J["2 × (Rz–Ry–Rz on 3 qubits + CNOT ring)<br/>18 trainable angles, shared over tokens"]
    J --> K["9 single-qubit X/Y/Z + 3 pair ZZ<br/>12D Pauli readout per token"]
    F --> L["20D per-token concatenation"]
    K --> L
    L --> M["Linear 20 → 32 + CLS/position embeddings<br/>one 4-head transformer encoder"]
    M --> N["Stage 2 verifier:<br/>ship / false-alarm score"]
    N -. "optional, not experimentally validated" .-> P["Possible future score re-ranking"]
    B -. "detector confidence" .-> P
\`\`\`

Only **candidate-level verifier performance** is evaluated in this research. The optional detector-score combination shown by a dashed path is an integration proposal; final detection AP50/mAP50–95 superiority was **not measured**.

**Figure 1: simulated QBloch transformation.** Three polarization-pair states are tensored into an 8×8 density matrix. Both trainable layers use three qubits × (Rz, Ry, Rz) and each is followed by the directed CNOT ring 0→1→2→0. The 18 shared trainable angles and 12 Pauli readouts are confirmed in the architecture/model test. These are classical matrix operations, not QPU operations.

**Figure 2: local feature fusion.** Each of 36 patches supplies an 8D handcrafted PolSAR descriptor and a 12D QBloch readout. Their 20D concatenation is projected to 32D, aggregated with a CLS token and positional embeddings by a one-layer, four-head transformer, and classified as a candidate-level ship/false-alarm decision.

**Input clarification:** PauliYOLOv8n operates on **PauliRGB pseudo-colour imagery**; the proposed verifier extracts **co-registered full-pol C9 channels** at detector candidate boxes. A diagram that sends the nine C9 real channels directly into stage-one PauliYOLO misstates the manuscript's input relationship.


**Primary source:** `notebooks/EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb`, specifically the candidate-token routines and `ThreeQubitUnitary`, `Arch2QuantumFeature`, `Arch2ControlFeature`, `TokenArch2Fusion`, and `SharedPoolHead`.

## Data path

1. **Candidate proposals**: PauliYOLOv8n on PauliRGB pseudo-colour imagery; inference conf=0.001, NMS IoU=0.65, max detections=300. Proposal boxes then locate co-registered full-pol C9 candidate chips.
2. **ROI chip**: 64×64 pixels of nine real-valued channels:
   `C11, Re(C12), Im(C12), Re(C13), Im(C13), C22, Re(C23), Im(C23), C33`. These reconstruct a Hermitian 3×3 complex matrix C for each pixel.
3. **Spatial tokens**: 6×6 grid, so 36 patches. Patch-aggregated C is normalized by span to form a complex 3×3 rho; each patch produces an 8-vector:
   `[log1p(span), |g12|, |g13|, |g23|, arg(g12)/pi, arg(g13)/pi, arg(g23)/pi, normalized eigen-entropy]`.
4. **QBloch states**: three 2×2 polarization-pair density matrices from pairs (0,1), (0,2), (1,2), using normalized pairwise Stokes/Bloch coordinates. Tensor product gives a simulated 8×8 three-qubit density matrix. No QPU is used.
5. **Trainable circuit**: two layers of `Rz–Ry–Rz` for each of three qubits; after **each layer**, apply the CNOT ring in sequence `0→1`, `1→2`, `2→0`. The ordering matches the matrix composition in `ThreeQubitUnitary.matrix()`.
6. **Observables**: nine single-qubit `X/Y/Z` expectations plus three pair `ZZ` expectations yield **12 real-valued features per patch**.
7. **Fusion**: concatenate 8 classical and 12 QBloch features to 20 per-patch features, linearly project to `d_model=32`, append a learned CLS token and positions, run one 4-head transformer encoder layer, then binary classification.

## Main-model parameter count

| Item | Implemented | Counting |
|--|--:|--|
| QBloch feature branch | 18 | 2 layers × 3 qubits × 3 angles |
| Classical feature branch | 100 | Linear(9,4)=40; Linear(4,12)=60 |
| Shared remaining verifier | 10,529 | Both model totals minus their feature-branch counts |
| Token–QBloch whole verifier | 10,547 | Model registry + trainable-parameter enumeration |
| Token–Control whole verifier | 10,629 | Model registry + trainable-parameter enumeration |

**Correct shared remainder:** 10,547 − 18 = **10,529** and 10,629 − 100 = **10,529**.

The earlier draft's **12-parameter** statement was incorrect; the updated 18 November 2026 manuscript now correctly uses **18** angles and **CNOT rings after both trainable layers**. The reported whole-model counts remain unchanged.

## Boundaries

- *Quantum-inspired* means a differentiable, classically simulated small Hilbert-space feature map, **not** hardware-based quantum inference or demonstrated quantum advantage.
- The matched classical-control comparison supports a modest positive AUC shift; it does not isolate the entanglement ring as an independently beneficial component. The entangled-vs-unentangled AUC Wilcoxon comparison is not significant.
- Candidate-level tests do not justify an image-level confidence interval.
- This code includes a two-stage design but requires an externally obtained, separately trained PauliYOLO detector and FPSD image/label inputs for raw-data execution.
