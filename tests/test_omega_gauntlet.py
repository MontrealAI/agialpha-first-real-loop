
import tempfile
import unittest
from pathlib import Path
from agialpha_omega_gauntlet.core import run_experiment, replay_docket, falsification_audit

class OmegaGauntletTests(unittest.TestCase):
    def test_omega_gauntlet_run_replay_audit(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            challenge = td / "omega_challenge_packs"
            challenge.mkdir()
            out = td / "docket"
            summary = run_experiment(out, challenge)
            self.assertGreaterEqual(summary["B6_beats_B5_count"], 10)
            self.assertEqual(summary["hard_safety_total"], 0)
            self.assertEqual(replay_docket(out)["status"], "pass")
            self.assertEqual(falsification_audit(out)["status"], "pass")

if __name__ == "__main__":
    unittest.main()
