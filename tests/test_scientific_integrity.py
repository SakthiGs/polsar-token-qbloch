"""Scientific checks execute the actual architecture cell of the canonical notebook."""
import json
import math
from pathlib import Path
from types import SimpleNamespace
from typing import Callable, Dict, Tuple
import unittest
import numpy as np
import torch
import torch.nn as nn

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb"

def model_source():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code = next("".join(c["source"]) for c in nb["cells"]
                if "class ThreeQubitUnitary(nn.Module)" in "".join(c.get("source", [])))
    cfg = SimpleNamespace(token_dim=8, q_layers=2, arch2_obs_dim=12,
                          control_hidden_a2=4, d_model=32, heads=4, dropout=.1,
                          patch_grid=6, fidelity_init_alpha=.1, fidelity_center=True)
    scope = {"torch": torch, "nn": nn, "np": np, "math": math,
             "Exp37Config": type("Exp37Config", (), {}),
             "Dict": Dict, "Tuple": Tuple, "Callable": Callable, "CFG": cfg}
    exec(compile(code, NOTEBOOK.name, "exec"), scope)
    return scope

class ScientificIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        cls.scope = model_source()

    def test_parameter_counts(self):
        s = self.scope
        q = s["MODEL_REGISTRY"]["Token_Arch2Quantum_Fusion"][0](s["CFG"])
        c = s["MODEL_REGISTRY"]["Token_Arch2Control_Fusion"][0](s["CFG"])
        self.assertEqual(s["count_params"](q), 10547)
        self.assertEqual(s["count_params"](c), 10629)
        self.assertEqual(s["count_params"](q.feature_extractor), 18)
        self.assertEqual(s["count_params"](c.feature_extractor), 100)
        self.assertEqual(10629 - 10547, 100 - 18)

    def test_ansatz_unitarity(self):
        s = self.scope
        for entangle in (False, True):
            ansatz = s["ThreeQubitUnitary"](n_layers=2, entangle=entangle)
            unitary = ansatz.matrix()
            self.assertEqual(tuple(ansatz.theta.shape), (2,3,3))
            torch.testing.assert_close(unitary.conj().T @ unitary,
                torch.eye(8, dtype=torch.complex64), rtol=1e-5, atol=1e-5)

    def test_correct_pauli_y_sign(self):
        s = self.scope
        rho = torch.zeros(1,1,3,3,dtype=torch.complex64)
        rho[...,0,0] = .5; rho[...,1,1] = .5
        rho[...,0,1] = .2j; rho[...,1,0] = -.2j
        qubits, bloch = s["bloch_from_rho"](rho)
        self.assertAlmostEqual(bloch[0,0,1].item(), -.4, places=5)
        for index in range(3):
            torch.testing.assert_close(qubits[0,0,index],qubits[0,0,index].conj().T)

    def test_finite_fusion_output(self):
        s = self.scope
        rng = np.random.default_rng(9)
        a = rng.standard_normal((2,36,3,3)) + 1j * rng.standard_normal((2,36,3,3))
        rho = a @ np.conj(np.swapaxes(a,-1,-2))
        rho /= np.trace(rho,axis1=-2,axis2=-1)[...,None,None]
        model = s["MODEL_REGISTRY"]["Token_Arch2Quantum_Fusion"][0](s["CFG"]).eval()
        with torch.no_grad():
            logits = model(torch.tensor(rho,dtype=torch.complex64),torch.randn(2,36,8))
        self.assertEqual(tuple(logits.shape),(2,))
        self.assertTrue(torch.isfinite(logits).all().item())

if __name__ == "__main__":
    unittest.main()
