"""Release gate regressions for historically tracked sensitive file paths."""
import unittest
from scripts.scan_git_history import classify_sensitive_path


class HistoryPathSecurityTests(unittest.TestCase):
    def test_known_safe_paths(self):
        for path in (
            ".env.example",
            "configs/input_provenance.json",
            "results/summary/grid_per_seed_metrics.csv",
            "notebooks/EXP37_M1_M2_ENTANGLEMENT_BOOTSTRAP.ipynb",
            "docs/ARCHITECTURE.md",
        ):
            with self.subTest(path=path):
                self.assertIsNone(classify_sensitive_path(path))

    def test_sensitive_paths_are_rejected(self):
        examples = (
            ".env", ".env.local", "secrets/key.txt", "private/notes.md",
            "weights/best.pt", "data/FPSD/train.tif", "checkpoints/model.ckpt",
            "results/sample.jpg", "published-paper.pdf", "credentials.json",
            "source/service_account_key.json", "id_rsa", "models/params.npz",
        )
        for path in examples:
            with self.subTest(path=path):
                self.assertIsNotNone(classify_sensitive_path(path))


if __name__ == "__main__":
    unittest.main()
