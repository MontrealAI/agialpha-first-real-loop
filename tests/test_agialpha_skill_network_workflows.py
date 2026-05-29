import unittest
from pathlib import Path

WORKFLOWS = [
    ".github/workflows/agialpha-engine-003-network-compounding.yml",
    ".github/workflows/agialpha-engine-003-network-replay.yml",
    ".github/workflows/agialpha-engine-003-network-falsification-audit.yml",
    ".github/workflows/agialpha-engine-003-network-claim-gate.yml",
]


class TestAgialphaSkillNetworkWorkflows(unittest.TestCase):
    def test_engine_003_workflows_have_safe_permissions_and_no_pages_deploy(self):
        for workflow in WORKFLOWS:
            text = Path(workflow).read_text(encoding="utf-8")
            self.assertIn("workflow_dispatch", text)
            self.assertIn("schedule:", text)
            self.assertIn("contents: read", text)
            self.assertIn("actions: read", text)
            self.assertNotIn("pages: write", text)
            self.assertNotIn("deploy-pages", text)
            self.assertNotIn("auto-merge", text.lower())

    def test_lifecycle_workflow_runs_full_network_chain(self):
        text = Path(".github/workflows/agialpha-engine-003-network-compounding.yml").read_text(encoding="utf-8")
        for command in [
            "network-compounding-run",
            "network-compounding-replay",
            "network-compounding-falsification-audit",
            "network-compounding-validate",
            "network-compounding-build-data",
        ]:
            self.assertIn(command, text)


if __name__ == "__main__":
    unittest.main()
