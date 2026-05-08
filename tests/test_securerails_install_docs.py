from pathlib import Path
import unittest

class TestSecureRailsInstallDocs(unittest.TestCase):
    def test_install_docs_boundary(self):
        text = Path('docs/secure-rails/installable-action.md').read_text(encoding='utf-8').lower()
        self.assertIn('no secrets required', text)
        self.assertIn('no auto-merge', text)
        self.assertIn('human review required', text)
        self.assertIn('no evidence docket, no empirical sota claim', text)

    def test_release_doc_pinning(self):
        text = Path('docs/secure-rails/release-and-versioning.md').read_text(encoding='utf-8').lower()
        self.assertIn('commit sha', text)
        self.assertIn('main', text)
        self.assertIn('demos only', text)
