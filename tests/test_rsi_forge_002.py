import json, tempfile, unittest
from pathlib import Path
from rsi_forge_002.core import run_experiment, replay, default_kernel, default_state, write_json, verify_state, repair_state_hash, HARD_SAFETY, CLAIM_BOUNDARY

class TestRSIForge002(unittest.TestCase):
    def test_run_and_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)/"repo"; root.mkdir()
            write_json(root/"data/rsi_forge_002/current_kernel.json", default_kernel())
            write_json(root/"data/rsi_forge_002/latest_state.json", default_state(default_kernel()))
            out = Path(td)/"out"
            res = run_experiment(out, root, cycles=2, candidates_per_cycle=6, seed=37)
            self.assertTrue((out/"00_manifest.json").exists())
            self.assertTrue((out/"scoreboard.html").exists())
            self.assertGreaterEqual(res["summary"]["candidate_kernels_executed"], 12)
            rep = replay(out)
            self.assertTrue(rep["replay_pass"])
            for k in HARD_SAFETY:
                self.assertEqual(res["summary"]["safety_counters"][k], 0)

    def test_state_hash_detection(self):
        st = default_state(default_kernel())
        self.assertTrue(verify_state(st)["state_hash_ok"])
        st["cycle_index"] = 99
        self.assertFalse(verify_state(st)["state_hash_ok"])
        self.assertTrue(verify_state(repair_state_hash(st))["state_hash_ok"])

    def test_claim_boundary_present(self):
        self.assertIn("does not claim achieved AGI", CLAIM_BOUNDARY)
        self.assertIn("Evidence Docket", CLAIM_BOUNDARY)

if __name__ == "__main__":
    unittest.main()
