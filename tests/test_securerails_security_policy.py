TARGET='SECURITY.md'
import unittest
from pathlib import Path

class T(unittest.TestCase):
    def test_exists(self):
        self.assertTrue(Path(TARGET).exists())

