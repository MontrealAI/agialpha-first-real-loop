import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_post_merge_exists(self):
        self.assertTrue(Path('.github/workflows/rsi-governor-001-post-merge.yml').exists())
