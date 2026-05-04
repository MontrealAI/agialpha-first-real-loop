import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_docs_link(self):
        self.assertIn('work-vaults-mark-sovereigns.md',Path('README.md').read_text(encoding='utf-8'))
        self.assertIn('work-vaults-mark-sovereigns.md',Path('docs/secure-rails/README.md').read_text(encoding='utf-8'))
