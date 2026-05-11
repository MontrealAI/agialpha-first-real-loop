import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_docs_exist(self):
        self.assertTrue(Path('docs/secure-rails/repository-security-baseline.md').exists())
