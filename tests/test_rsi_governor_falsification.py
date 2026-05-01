import json
import tempfile
import unittest
from pathlib import Path

from agialpha_rsi_governor.falsification import falsification_report


class TestRSIGovernorFalsification(unittest.TestCase):
    def test_falsification_passes_when_required_files_exist(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "07_evaluation_results").mkdir(parents=True)
            (d / "13_promotion_dossier").mkdir(parents=True)
            (d / "00_manifest.json").write_text(json.dumps({"ok": True}))
            (d / "07_evaluation_results/heldout_results.json").write_text(json.dumps({"ok": True}))
            (d / "13_promotion_dossier/promotion_dossier.md").write_text("ok")
            report = falsification_report(d)
            self.assertTrue(report["falsification_pass"])


if __name__ == "__main__":
    unittest.main()
