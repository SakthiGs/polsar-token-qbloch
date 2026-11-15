"""Synthetic prediction files test the no-imagery metrics reconstruction script."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pred", ROOT / "scripts" / "reproduce_from_predictions.py")
pred = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pred)

class TestPredictionPipeline(unittest.TestCase):
    def test_prediction_reconstruction(self):
        rng = np.random.default_rng(11)
        labels = np.array([0]*30+[1]*30)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sources = root/"predictions"
            sources.mkdir()
            for model in (pred.PRIMARY_Q,pred.PRIMARY_C,pred.NOENT):
                for seed in (42,43):
                    scores = np.clip(labels*.65+.15+rng.normal(0,.15,len(labels)),.00001,.99999)
                    if model==pred.PRIMARY_C:
                        scores = np.clip(scores+rng.normal(0,.05,len(labels)),.00001,.99999)
                    np.savez_compressed(sources/f"{model}_seed{seed}.npz",
                        prob=scores,label=labels,
                        image_id=np.array([f"im{i//3}" for i in range(len(labels))]),
                        seed=np.array(seed),model=np.array(model))
            rows, boot = pred.compute(sources,root/"outputs",[42,43],32)
            self.assertEqual(len(rows),6)
            self.assertEqual(len(boot),6)
            self.assertEqual({row["level"] for row in boot},{"candidate","image"})
            self.assertTrue((root/"outputs"/"paired_bootstrap.csv").is_file())

if __name__ == "__main__":
    unittest.main()
