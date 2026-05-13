from pathlib import Path
import unittest
class T(unittest.TestCase):
  def test_exists(self):
    s=Path('.github/ISSUE_TEMPLATE/securerails-human-review.yml').read_text(); self.assertIn('Review type',s); self.assertIn('needs-decision',s)
