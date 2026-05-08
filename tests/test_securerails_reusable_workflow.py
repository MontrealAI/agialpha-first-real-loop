from pathlib import Path
import unittest

class TestSecureRailsReusableWorkflow(unittest.TestCase):
    def test_reusable_workflow_safety(self):
        txt = Path('.github/workflows/securerails-pr-guard-reusable.yml').read_text(encoding='utf-8')
        self.assertIn('workflow_call', txt)
        self.assertIn('contents: read', txt)
        self.assertIn('pull-requests: read', txt)
        self.assertIn('actions: read', txt)
        self.assertNotIn('pull_request_target', txt)
        self.assertNotIn('write', txt)
        self.assertNotIn('secrets:', txt)
