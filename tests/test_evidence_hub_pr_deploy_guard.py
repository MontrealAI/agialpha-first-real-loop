import unittest
from pathlib import Path


class TestEvidenceHubPRDeployGuard(unittest.TestCase):
    def test_deploy_guard_is_main_and_trusted_events_only(self):
        wf = Path('.github/workflows/evidence-hub-publish.yml').read_text()
        self.assertIn("github.repository == 'MontrealAI/agialpha-first-real-loop'", wf)
        self.assertIn("github.ref == 'refs/heads/main'", wf)
        self.assertIn("github.event_name == 'push'", wf)
        self.assertIn("github.event_name == 'workflow_dispatch'", wf)
        self.assertIn("github.event_name == 'schedule'", wf)
        self.assertIn("github.event_name == 'repository_dispatch'", wf)

    def test_pr_mode_prints_deploy_skip_message(self):
        wf = Path('.github/workflows/evidence-hub-publish.yml').read_text()
        self.assertIn('Build/validate completed. Deployment skipped because this is not main.', wf)
        self.assertIn('pull_request:', wf)


if __name__ == '__main__':
    unittest.main()
