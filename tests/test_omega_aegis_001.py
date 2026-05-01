import json
import tempfile
import unittest
from pathlib import Path
from omega_aegis_001.core import run_experiment, verify_docket, audit_docket

class OmegaAegisTest(unittest.TestCase):
    def test_run_verify_audit(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "run"
            manifest = run_experiment(str(out))
            self.assertEqual(manifest["status"], "success")
            self.assertEqual(manifest["metrics"]["B6_false_accepts"], 0)
            self.assertEqual(manifest["metrics"]["safety_incidents"], 0)
            report = verify_docket(str(out / "evidence-docket"), manifest["root_hash"])
            self.assertEqual(report["status"], "pass")
            audit = audit_docket(str(out / "evidence-docket"))
            self.assertEqual(audit["status"], "pass")

    def test_vnext(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "vnext"
            manifest = run_experiment(str(out), variant="vnext")
            self.assertEqual(manifest["metrics"]["B6_false_accepts"], 0)
            self.assertGreaterEqual(manifest["metrics"]["B6_attack_catch_rate_pct"], 100)

if __name__ == "__main__":
    unittest.main()
