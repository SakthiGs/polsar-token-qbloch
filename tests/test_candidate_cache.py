"""Exercise cache invalidation and candidate/feature metadata alignment."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
import numpy as np
import pandas as pd

NOTEBOOK = Path(__file__).resolve().parents[1] / "notebooks" / "EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb"

class TestCandidateCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        src = next("".join(c["source"]) for c in nb["cells"]
                   if "def cache_manifest(" in "".join(c.get("source", [])))
        scope = {
            "Path": Path, "hashlib": hashlib, "json": json, "np": np, "pd": pd,
            "Exp37Config": type("Exp37Config", (), {}),
            "_exists": lambda p: bool(p) and Path(p).exists(),
            "CACHE_DIR": Path(tempfile.gettempdir())
        }
        exec(src[src.index("def _sha256_file"):src.index("def yolo_candidates")], scope)
        cls.funcs = scope
        cls.extract_source = src[src.index("def extract_split_from_candidates"):src.index("def get_real_split")]

    def test_cache_fingerprint_changes_with_weights_or_annotations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for dirname in ("images", "tif"):
                (root / dirname).mkdir()
            (root / "images" / "a.jpg").write_bytes(b"image")
            (root / "tif" / "a.tif").write_bytes(b"data")
            (root / "ann.json").write_text('{"images":[]}')
            (root / "best.pt").write_bytes(b"first detector")
            cfg = SimpleNamespace(
                yolo_best=str(root/"best.pt"), train_image_dir=str(root/"images"),
                train_tif_dir=str(root/"tif"), train_ann=str(root/"ann.json"),
                val_image_dir=str(root/"images"), val_tif_dir=str(root/"tif"),
                val_ann=str(root/"ann.json"), imgsz=640, yolo_conf=.001, yolo_iou=.65,
                max_det=300, iou_eval=.5, chip_size=64, patch_grid=6,
                c9_layout="fpsd_exp25_9", symmetrize_c9=True, eps=1e-8, token_dim=8
            )
            f = self.funcs["cache_key"]
            before = f(cfg,"val")
            (root/"best.pt").write_bytes(b"second detector")
            after_weights = f(cfg,"val")
            self.assertNotEqual(before,after_weights)
            (root/"ann.json").write_text('{"images":[1]}')
            self.assertNotEqual(after_weights,f(cfg,"val"))

    def test_extracted_candidate_metadata_matches_feature_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/"b.tif").write_bytes(b"placeholder")
            rows = [
                dict(stem="a",image_id=10,x1=1.,y1=2.,x2=3.,y2=4.,candidate_label=0),
                dict(stem="b",image_id=11,x1=2.,y1=2.,x2=6.,y2=6.,candidate_label=1),
                dict(stem="b",image_id=11,x1=6.,y1=6.,x2=8.,y2=8.,candidate_label=0)
            ]
            class FakeReader:
                def __init__(self,*args): pass
                def read_c9_chip(self,*args): return None
                def close(self): pass
            scope = {
                "Path": Path, "np": np, "pd": pd,
                "Exp37Config": type("Exp37Config", (), {}),
                "C9ImageReader": FakeReader,
                "chip_to_tokens": lambda *a: (np.zeros((36,8),np.float32),
                    np.eye(3,dtype=np.complex64)[None].repeat(36,axis=0))
            }
            exec(self.extract_source, scope)
            rho, tokens, y, meta = scope["extract_split_from_candidates"](
                pd.DataFrame(rows), root, SimpleNamespace(chip_size=64))
            self.assertEqual(len(y),2)  # missing TIFF 'a' excluded
            self.assertEqual(len(meta),len(y))
            self.assertEqual(meta["image_id"].tolist(),[11,11])
            self.assertEqual(meta["candidate_label"].tolist(),y.astype(int).tolist())

if __name__ == "__main__":
    unittest.main()
