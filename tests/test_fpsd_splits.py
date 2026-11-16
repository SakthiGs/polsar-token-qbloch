"""Filename-based FPSD split audit tests; COCO IDs can overlap across splits."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_fpsd_splits import verify_splits

def make_coco(path, names, ids):
    images = [{"id": image_id, "file_name": filename} for filename, image_id in zip(names, ids)]
    payload = {"images": images, "annotations": [
        {"id": idx+1, "image_id": img["id"], "category_id": 0}
        for idx, img in enumerate(images)]}
    path.write_text(json.dumps(payload), encoding="utf-8")

class SplitAuditTests(unittest.TestCase):
    def test_repeated_numeric_ids_across_splits_are_not_leakage(self):
        with tempfile.TemporaryDirectory() as root:
            folder=Path(root)
            train=folder/"train.json";val=folder/"val.json"
            make_coco(train,["001.tif","002.tif"],[1,2])
            make_coco(val,["003.tif"],[1])
            out=verify_splits(train,val)
            self.assertEqual(out["overlapping_filenames"],0)
            self.assertEqual(out["overlapping_local_coco_image_ids"],1)

    def test_same_filename_is_rejected_even_when_ids_differ(self):
        with tempfile.TemporaryDirectory() as root:
            folder=Path(root)
            train=folder/"train.json";val=folder/"val.json"
            make_coco(train,["001.tif"],[100])
            make_coco(val,["001.tif"],[200])
            with self.assertRaisesRegex(ValueError,"filename overlap"):
                verify_splits(train,val)

    def test_annotations_with_missing_image_id_are_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            folder=Path(root)
            train=folder/"train.json";val=folder/"val.json"
            make_coco(train,["001.tif"],[100])
            make_coco(val,["002.tif"],[200])
            x=json.loads(val.read_text())
            x["annotations"][0]["image_id"]=900
            val.write_text(json.dumps(x))
            with self.assertRaisesRegex(ValueError,"absent images"):
                verify_splits(train,val)

if __name__=="__main__":
    unittest.main()
