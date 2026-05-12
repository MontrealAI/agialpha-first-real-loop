import unittest
from secure_rails.policy_kernel import evaluate_file


class T(unittest.TestCase):
    def test_invalid_work_vault_rejects_false_required_flags(self):
        decision = evaluate_file('tests/fixtures/securerails_policy/invalid_work_vault_no_human_review.json')
        self.assertEqual(decision['decision'], 'reject')

    def test_valid_work_vault_allows_or_warns(self):
        decision = evaluate_file('tests/fixtures/securerails_policy/valid_work_vault.json')
        self.assertIn(decision['decision'], ['allow', 'warn', 'escalate'])


if __name__ == '__main__':
    unittest.main()
