import unittest
from pathlib import Path

class T(unittest.TestCase):
  def test_workflow(self):
    p=Path('.github/workflows/securerails-trust-center-001.yml'); self.assertTrue(p.exists()); txt=p.read_text().lower(); self.assertNotIn('deploy-pages',txt)
