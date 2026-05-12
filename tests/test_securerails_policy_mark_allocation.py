import unittest
from secure_rails.policy_kernel import evaluate_file


class TestSecureRailsPolicyMarkAllocation(unittest.TestCase):
    def test_invalid_mark_automerge_rejected(self):
        d = evaluate_file('tests/fixtures/securerails_policy/invalid_mark_automerge.json', context_type='mark_allocation')
        self.assertEqual(d['decision'], 'reject')

    def test_valid_mark_allocation_allow_or_warn(self):
        d = evaluate_file('tests/fixtures/securerails_policy/valid_mark_allocation.json', context_type='mark_allocation')
        self.assertEqual(d['decision'], 'escalate')


if __name__ == '__main__':
    unittest.main()
