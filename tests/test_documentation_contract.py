"""Check that the README architecture stays aligned with verified code contracts."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class DocumentationContract(unittest.TestCase):
    def test_main_architecture_is_present(self):
        readme=(ROOT/"README.md").read_text(encoding="utf-8")
        for item in ("mermaid","PauliYOLOv8n","36 patches","8D","12D","20D",
                     "Rz–Ry–Rz","CNOT","10,547","10,629","18"):
            self.assertIn(item,readme)
        self.assertIn("not",readme.lower())
        self.assertIn("simulated",readme.lower())

    def test_release_gate_clearly_private(self):
        release=(ROOT/"docs"/"RELEASE_READINESS.md").read_text(encoding="utf-8")
        self.assertIn("PRIVATE",release)
        self.assertIn("license",release.lower())
        self.assertIn("raw",release.lower())

if __name__=="__main__":
    unittest.main()
