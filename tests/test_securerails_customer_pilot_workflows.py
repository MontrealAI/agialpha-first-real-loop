import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_smoke(self):
        self.assertTrue(Path('docs/secure-rails/customer-pilot-intake.md').exists())
