import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_workflows_exist(self):
        self.assertTrue(Path('.github/workflows/securerails-repo-security-baseline-001.yml').exists())
        self.assertTrue(Path('.github/workflows/securerails-dependency-review-001.yml').exists())
