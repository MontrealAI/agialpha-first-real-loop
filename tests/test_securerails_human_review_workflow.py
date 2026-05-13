from pathlib import Path
import unittest
class T(unittest.TestCase):
  def test_workflow(self):
    s=Path('.github/workflows/securerails-human-review-console-001.yml').read_text(); self.assertIn('contents: read',s); self.assertNotIn('deploy-pages',s)
