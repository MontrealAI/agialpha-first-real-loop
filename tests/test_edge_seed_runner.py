import tempfile
import unittest
from pathlib import Path
from agialpha_seed_runner import core

class EdgeSeedRunnerTests(unittest.TestCase):
    def test_claim_boundary_mentions_no_autonomous_promotion(self):
        self.assertIn("autonomous claim promotion is not", core.CLAIM_BOUNDARY)

    def test_required_status_missing(self):
        with tempfile.TemporaryDirectory() as td:
            status = core.required_status(Path(td))
            self.assertFalse(status["base_complete"])
            self.assertGreater(len(status["missing_base"]), 0)

    def test_hash_manifest_empty(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.txt").write_text("x", encoding="utf-8")
            hm = core.hash_manifest(root)
            self.assertEqual(hm["file_count"], 1)
            self.assertTrue(hm["root_sha256"])

if __name__ == "__main__":
    unittest.main()
