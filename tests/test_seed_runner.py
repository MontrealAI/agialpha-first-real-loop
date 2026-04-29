
import tempfile
import unittest
from pathlib import Path

from agialpha_seed_runner.core import run_seed_runner, independent_replay, write_json

class SeedRunnerSmokeTest(unittest.TestCase):
    def test_seed_runner_exports_dockets(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base = root / "evidence-docket"
            base.mkdir()
            for name in [
                "00_manifest.json", "01_seed_001.json", "02_mark_review_card.json",
                "03_sovereign_001.json", "04_job_outputs.json", "05_sources_used.json",
                "06_accepted_interventions.json", "07_coldchain_energy_compiler_v0.json",
                "08_seed_002.json", "09_treatment_control_comparison.json"
            ]:
                write_json(base / name, {})
            (base / "10_decision_memo.md").write_text("PASSED", encoding="utf-8")
            (base / "REPLAY_INSTRUCTIONS.md").write_text("replay", encoding="utf-8")
            index = run_seed_runner(base, root / "seed-dockets", 2)
            self.assertEqual(index["count"], 2)
            self.assertTrue((root / "seed-dockets" / "seed-001" / "claim_level.json").exists())
            report = independent_replay(root / "seed-dockets", root / "replay")
            self.assertEqual(report["failed"], 0)
            self.assertEqual(report["passed"], 2)

if __name__ == "__main__":
    unittest.main()
