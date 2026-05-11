import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_no_certification_term(self):
        txt=Path('docs/secure-rails/repository-security-baseline.md').read_text().lower()
        self.assertNotIn('guaranteed security',txt)
