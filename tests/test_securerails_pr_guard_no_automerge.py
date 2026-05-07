import unittest
from secure_rails_pr_guard.no_automerge import review_no_automerge
class T(unittest.TestCase):
  def test_block(self): self.assertTrue(review_no_automerge({"a":"enable-pull-request-automerge"})["findings"])
