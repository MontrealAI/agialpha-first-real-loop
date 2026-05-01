import pathlib, tempfile, unittest
from agialpha_rsi_forge_001.run import run
from agialpha_rsi_forge_001.replay import replay
from agialpha_rsi_forge_001.audit import audit
from agialpha_rsi_forge_001.vnext import vnext

class TestRSIForge001(unittest.TestCase):
    def test_run_replay_audit_vnext(self):
        with tempfile.TemporaryDirectory() as td:
            out = pathlib.Path(td) / "docket"
            s = run(out, cycles=5, candidates_per_cycle=4)
            self.assertGreater(s["b6_heldout_advantage_vs_b5"], 0)
            self.assertGreater(s["heldout_improvement_from_seed"], 0)
            self.assertEqual(s["safety_incidents"], 0)
            self.assertEqual(replay(out)["status"], "pass")
            self.assertEqual(audit(out)["status"], "pass")
            self.assertEqual(vnext(out)["status"], "pass")
            self.assertTrue((out / "03_kernel_lineage" / "lineage.json").exists())
            self.assertTrue((out / "evidence-run-manifest.json").exists())
            self.assertTrue((out / "scoreboard.html").exists())

if __name__ == "__main__":
    unittest.main()
