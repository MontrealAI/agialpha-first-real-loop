import unittest
from pathlib import Path
class T(unittest.TestCase):
  def test_workflow_permissions(self):
    t=Path('.github/workflows/securerails-e2e-pilot-canary-001.yml').read_text()
    self.assertIn('contents: read',t); self.assertNotIn('pages: write',t)
