from pathlib import Path
import unittest
class T(unittest.TestCase):
  def test_exists(self): s=Path('.github/PULL_REQUEST_TEMPLATE/securerails-safe-remediation.md').read_text(); self.assertIn('No auto-merge',s); self.assertIn('Human reviewer decision recorded',s)
