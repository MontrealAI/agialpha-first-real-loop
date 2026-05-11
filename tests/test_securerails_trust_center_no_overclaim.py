import unittest
from pathlib import Path

class T(unittest.TestCase):
  def test_no_overclaim(self):
    txt='\n'.join(Path('docs/secure-rails').glob('*.md') and [p.read_text().lower() for p in Path('docs/secure-rails').glob('*.md')])
    for bad in ['guaranteed security','eu ai act exempt','cybersecurity certified','nist certified','iso 27001 certified','soc 2 certified']:
      self.assertNotIn(bad,txt)
