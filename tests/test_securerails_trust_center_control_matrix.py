import unittest
from pathlib import Path

class T(unittest.TestCase):
    def test_matrix(self):
        p=Path('docs/secure-rails/trust-center-control-matrix.md'); self.assertTrue(p.exists()); txt=p.read_text().lower(); self.assertNotIn('soc 2 certified',txt)
