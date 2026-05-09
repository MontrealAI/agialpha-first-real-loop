import unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_workflows(self):
        for p in ['.github/workflows/securerails-template-bootstrap-001.yml','.github/workflows/securerails-template-health-check-001.yml']:
            self.assertTrue(Path(p).exists())
