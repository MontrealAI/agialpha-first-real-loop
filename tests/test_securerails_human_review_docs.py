from pathlib import Path
import unittest
class T(unittest.TestCase):
  def test_docs(self):
    s=Path('docs/secure-rails/reviewer-guide.md').read_text().lower(); self.assertIn('manual merge',s); self.assertIn('human review',s)
