from pathlib import Path
import unittest


class TestEvidenceHubPrDeployGuard(unittest.TestCase):
    def test_central_workflow_has_trusted_main_guard(self):
        text = Path('.github/workflows/evidence-hub-publish.yml').read_text()
        self.assertIn("github.repository == 'MontrealAI/agialpha-first-real-loop'", text)
        self.assertIn("github.ref == 'refs/heads/main'", text)
        self.assertIn("github.event_name == 'push'", text)
        self.assertIn("github.event_name == 'workflow_dispatch'", text)
        self.assertIn("github.event_name == 'schedule'", text)
        self.assertIn("github.event_name == 'repository_dispatch'", text)

    def test_pull_request_trigger_exists_for_build_validate(self):
        text = Path('.github/workflows/evidence-hub-publish.yml').read_text()
        self.assertIn("pull_request:", text)
        self.assertIn("Deployment skipped because this is not main", text)


if __name__ == '__main__':
    unittest.main()
