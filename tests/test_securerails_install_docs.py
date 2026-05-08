from pathlib import Path
import unittest

class TestSecureRailsInstallDocs(unittest.TestCase):
    def test_install_docs_posture(self):
        txt = Path('docs/secure-rails/installable-action.md').read_text(encoding='utf-8').lower()
        self.assertIn('pin to a release tag or commit sha', txt)
        self.assertIn('not `main`', txt)
        self.assertIn('no secrets required', txt)
        self.assertIn('no auto-merge', txt)
        self.assertIn('no evidence docket, no empirical sota claim', txt)
