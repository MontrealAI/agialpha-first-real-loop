from pathlib import Path
import unittest

class TestSecureRailsActionMetadata(unittest.TestCase):
    def test_action_metadata(self):
        p = Path('.github/actions/securerails-pr-guard/action.yml')
        self.assertTrue(p.exists())
        txt = p.read_text(encoding='utf-8')
        for key in ['name:', 'description:', 'inputs:', 'outputs:', 'mode:', 'recommendation:']:
            self.assertIn(key, txt)
