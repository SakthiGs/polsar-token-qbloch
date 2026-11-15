# Verified parameter-count correction (SEQUENCE 2026 Paper #67)

The reviewed manuscript reported 12 trainable quantum-branch parameters, but the implemented two-layer ansatz has 3 qubits and 3 trainable rotation angles per qubit, i.e. 18 total.

| Model | Branch | Whole verifier |
|---|---:|---:|
| Token–QBloch Fusion | 18 | 10,547 |
| Token–Control Fusion | 100 | 10,629 |

Differences: 100 − 18 = 82 and 10,629 − 10,547 = 82.

The implemented trainable rotations are Rz–Ry–Rz for each qubit per layer. Inspect the circuit construction to describe all CNOT entangling rings precisely; do not use the old R_y/R_z-only two-layer illustration.

The correction is documentary, not a license to alter the archived AP/AUC/F1 statistics. Recount trainable parameters using the exact saved implementation before final publication.

Related camera-ready work remains: Springer table layout/captions, abstract paragraph break, ORCID command, signed License-to-Publish, correctly marked revision notes, and highlighted/clean PDF consistency.
