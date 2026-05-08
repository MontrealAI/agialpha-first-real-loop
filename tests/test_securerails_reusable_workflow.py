from pathlib import Path
import unittest

class TestSecureRailsReusableWorkflow(unittest.TestCase):
    def test_workflow_safety(self):
        text = Path('.github/workflows/securerails-pr-guard-reusable.yml').read_text(encoding='utf-8')
        self.assertIn('workflow_call', text)
        self.assertIn('contents: read', text)
        self.assertIn('pull-requests: read', text)
        self.assertIn('actions: read', text)
        self.assertNotIn('pull_request_target', text)
        self.assertNotIn('secrets:', text)
        self.assertNotIn(': write', text)
