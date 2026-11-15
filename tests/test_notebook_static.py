"""Static source portability tests; run with Python stdlib unittest."""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]

class TestPortableNotebooks(unittest.TestCase):
    def test_clean_sources(self):
        items=sorted((ROOT/"notebooks").glob("EXP37_*.ipynb"))
        self.assertEqual(2,len(items))
        for path in items:
            nb=json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(nb["cells"])
            code="\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"]=="code")
            for token in ("/content/drive", "/mnt/data", "MyDrive/"):
                self.assertNotIn(token,code)
            self.assertIn("POLSAR_DRY_RUN",code)
            self.assertIn("POLSAR_FPSD_ROOT",code)
            self.assertNotIn("split validation candidates 80/20",code)
            for c in nb["cells"]:
                if c["cell_type"]=="code":
                    self.assertFalse(c["outputs"])
                    self.assertIsNone(c["execution_count"])
                    compile("".join(c["source"]),path.name,"exec")

if __name__=="__main__":
    unittest.main()
