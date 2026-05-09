import unittest
from secure_rails.release_notes import render_notes
class T(unittest.TestCase):
  def test_sections(self):
    s=render_notes({'release_version':'0.1.0-rc1','release_channel':'rc','claim_boundary':'x'})
    self.assertIn('Human review requirement',s)
