import tempfile
import unittest
from pathlib import Path
from agialpha_helios import core

class HeliosTest(unittest.TestCase):
    def test_run_replay_audit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "helios"
            summary = core.run(root)
            self.assertEqual(summary["task_count"], 6)
            self.assertEqual(summary["safety_incidents"], 0)
            self.assertTrue(summary["all_tasks_B6_win"])
            self.assertTrue((root / "EnergyComputeResilienceCompiler-v0.json").exists())
            replay = core.replay(root)
            self.assertEqual(replay["status"], "pass")
            audit = core.falsification_audit(root)
            self.assertEqual(audit["status"], "pass")

if __name__ == "__main__":
    unittest.main()
