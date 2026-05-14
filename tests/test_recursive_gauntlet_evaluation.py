import unittest, tempfile, subprocess, json
from pathlib import Path
class T(unittest.TestCase):
    def test_ok(self):
        root=Path(__file__).resolve().parents[1]
        self.assertTrue((root/'agialpha_recursive_gauntlet').exists())
