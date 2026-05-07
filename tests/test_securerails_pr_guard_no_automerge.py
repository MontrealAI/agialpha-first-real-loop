import unittest
from secure_rails_pr_guard.no_automerge import review_no_automerge
class T(unittest.TestCase):
  def test_block_enablement_pattern(self):
    self.assertTrue(review_no_automerge({"a":"gh pr merge 12 --auto"})["findings"])

  def test_ignore_policy_text(self):
    self.assertFalse(review_no_automerge({"a":"Do not use auto-merge in this repository."})["findings"])
