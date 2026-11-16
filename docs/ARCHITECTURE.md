# Implemented EXP37 architecture — source-aligned technical note

**Primary source:** `notebooks/EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb`, specifically the candidate-token routines and `ThreeQubitUnitary`, `Arch2QuantumFeature`, `Arch2ControlFeature`, `TokenArch2Fusion`, and `SharedPoolHead`.

## Data path

1. **Candidate proposals**: PauliYOLOv8n; inference conf=0.001, NMS IoU=0.65, max detections=300.
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

The paper's older **12-parameter** description is incorrect. Correct the paper text and Figure 1 to 18 angles and **CNOT rings after both layers**, without changing the experimentally verified reported totals.

## Boundaries

- *Quantum-inspired* means a differentiable, classically simulated small Hilbert-space feature map, **not** hardware-based quantum inference or demonstrated quantum advantage.
- The matched classical-control comparison supports a modest positive AUC shift; it does not isolate the entanglement ring as an independently beneficial component. The entangled-vs-unentangled AUC Wilcoxon comparison is not significant.
- Candidate-level tests do not justify an image-level confidence interval.
- This code includes a two-stage design but requires an externally obtained, separately trained PauliYOLO detector and FPSD image/label inputs for raw-data execution.
