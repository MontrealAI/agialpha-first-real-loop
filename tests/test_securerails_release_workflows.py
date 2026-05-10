import unittest
from pathlib import Path
class T(unittest.TestCase):
  def test_no_auto_publish(self):
    t=Path('.github/workflows/securerails-release-candidate-001.yml').read_text(); self.assertIn('workflow_dispatch',t)
