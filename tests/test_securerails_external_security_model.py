from pathlib import Path
import unittest

class TestSecureRailsExternalSecurityModel(unittest.TestCase):
    def test_security_model_boundaries(self):
        txt = Path('docs/secure-rails/external-repo-security-model.md').read_text(encoding='utf-8').lower()
        for phrase in ['human review required', 'no auto-merge', 'no secrets required', 'not cybersecurity-certification', 'not legal approval']:
            self.assertIn(phrase, txt)
