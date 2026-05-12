from pathlib import Path
import unittest
class T(unittest.TestCase):
  def test_boundary(self):
    s=Path('docs/secure-rails/human-review-console.md').read_text().lower(); self.assertNotIn('certified secure',s); self.assertNotIn('dividends',s)
