import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_heldout_exists(self):
        self.assertTrue(Path("rsi_governor_tasks/heldout/tasks.json").exists())
