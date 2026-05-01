import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_exists(self):
        self.assertTrue(Path('README.md').exists())
if __name__=='__main__': unittest.main()
