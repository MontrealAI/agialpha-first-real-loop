import unittest
from secure_rails.release_notes import render_notes
class T(unittest.TestCase):
  def test_token_boundary(self): self.assertIn('utility-only',render_notes({'release_version':'1','release_channel':'rc','claim_boundary':'x'}))
