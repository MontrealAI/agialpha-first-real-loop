import tempfile
import unittest
from pathlib import Path

from agialpha_cyber_sovereign2.core import run_experiment, replay_docket, audit_docket, CLAIM_BOUNDARY


class CyberSovereign2Tests(unittest.TestCase):
    def test_cyber_sovereign_002_generates_docket(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            repo.mkdir()
            (repo / ".github" / "workflows").mkdir(parents=True)
            (repo / ".github" / "workflows" / "demo.yml").write_text("name: demo\non: push\npermissions:\n  contents: read\n", encoding="utf-8")
            out = root / "docket"
            summary = run_experiment(out, repo)
            self.assertEqual(summary["experiment"], "CYBER-SOVEREIGN-002")
            self.assertEqual(summary["raw_secret_leak_count"], 0)
            self.assertTrue((out / "13_security_capability_archive" / "CyberSecurityCapabilityArchive-v1.json").exists())
            self.assertTrue((out / "16_safety_ledgers" / "safety_ledger.json").exists())
            self.assertIn(CLAIM_BOUNDARY, (out / "00_manifest.json").read_text(encoding="utf-8"))

    def test_replay_and_audit_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            repo.mkdir()
            (repo / ".github" / "workflows").mkdir(parents=True)
            (repo / ".github" / "workflows" / "demo.yml").write_text("name: demo\non: push\n", encoding="utf-8")
            docket = root / "docket"
            run_experiment(docket, repo)
            replay = replay_docket(docket, root / "replay")
            audit = audit_docket(docket, root / "audit")
            self.assertEqual(replay["replay_status"], "pass")
            self.assertEqual(audit["verdict"], "pass")


if __name__ == "__main__":
    unittest.main()
