import json
import tempfile
import unittest
from pathlib import Path

from agialpha_benchmark_gauntlet.core import generate_docket, replay_docket, falsification_audit


class BenchmarkGauntletTest(unittest.TestCase):
    def test_generate_replay_and_audit(self):
        with tempfile.TemporaryDirectory() as td:
            docket = Path(td) / "benchmark-gauntlet-001-evidence-docket"
            result = generate_docket(docket)
            summary = result["summary"]
            self.assertGreaterEqual(summary["task_count"], 9)
            self.assertGreater(summary["B6_beats_B5_count"], 0)
            self.assertTrue(all(v == 0 for v in summary["hard_safety"].values()))
            replay = replay_docket(docket)
            self.assertTrue(replay["replay_pass"])
            audit = falsification_audit(docket)
            self.assertTrue(audit["passed"])
            self.assertTrue((docket / "06_proof_bundles").exists())


if __name__ == "__main__":
    unittest.main()
