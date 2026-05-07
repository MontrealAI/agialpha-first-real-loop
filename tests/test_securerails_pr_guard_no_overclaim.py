import unittest
from secure_rails_pr_guard.claim_boundary import review_claims
class T(unittest.TestCase):
  def test_claims(self): self.assertTrue(review_claims({"a":"guaranteed security"})["violations"])
