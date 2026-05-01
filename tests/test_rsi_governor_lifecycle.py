import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_workflow_exists(self):
        self.assertTrue(Path('.github/workflows/rsi-governor-001-lifecycle.yml').exists())
