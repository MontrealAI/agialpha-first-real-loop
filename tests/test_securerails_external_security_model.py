from pathlib import Path
import unittest

class TestSecureRailsExternalSecurityModel(unittest.TestCase):
    def test_model_content(self):
        text = Path('docs/secure-rails/external-repo-security-model.md').read_text(encoding='utf-8').lower()
        for phrase in ['untrusted', 'no auto-merge', 'no secrets required', 'human review required', 'cybersecurity-certification']:
            self.assertIn(phrase, text)
