import json
import tempfile
import unittest
from pathlib import Path
from agialpha_first_loop.core import build_evidence_docket

class FirstLoopReplayTests(unittest.TestCase):
    def test_loop_passes_and_outputs_required_files(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "loop"
            docket = build_evidence_docket(root, out)
            self.assertTrue(docket["loop_passed"])
            required = [
                "00_manifest.json",
                "01_seed_001.json",
                "02_mark_review_card.json",
                "03_sovereign_001.json",
                "04_job_outputs.json",
                "05_sources_used.json",
                "06_accepted_interventions.json",
                "07_coldchain_energy_compiler_v0.json",
                "08_seed_002.json",
                "09_treatment_control_comparison.json",
                "10_decision_memo.md",
                "REPLAY_INSTRUCTIONS.md",
            ]
            for name in required:
                self.assertTrue((out / name).exists(), name)

    def test_treatment_beats_control(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "loop"
            build_evidence_docket(root, out)
            comp = json.loads((out / "09_treatment_control_comparison.json").read_text())
            self.assertGreaterEqual(comp["reuse_lift"], 0.25)
            self.assertLessEqual(comp["hallucination_delta"], 0)
            self.assertLessEqual(comp["safety_delta"], 0)

if __name__ == "__main__":
    unittest.main()
