import unittest
from secure_rails.policy_kernel import evaluate_file
class T(unittest.TestCase):
    def test_negative_allowed(self): self.assertIn(evaluate_file('tests/fixtures/securerails_policy/allowed_negative_boundary.md')['decision'], ['allow','warn','escalate'])
    def test_overclaim_reject(self): self.assertEqual(evaluate_file('tests/fixtures/securerails_policy/forbidden_positive_overclaim.md')['decision'],'reject')
    def test_token_reject(self): self.assertEqual(evaluate_file('tests/fixtures/securerails_policy/forbidden_token_yield.md')['decision'],'reject')
if __name__=='__main__': unittest.main()
