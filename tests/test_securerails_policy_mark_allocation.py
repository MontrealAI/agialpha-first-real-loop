import unittest
from secure_rails.policy_kernel import evaluate_file


class TestSecureRailsPolicyMarkAllocation(unittest.TestCase):
    def test_invalid_mark_automerge_rejected(self):
        d = evaluate_file('tests/fixtures/securerails_policy/invalid_mark_automerge.json', context_type='mark_allocation')
        self.assertEqual(d['decision'], 'reject')

    def test_mark_human_review_false_rejected(self):
        import json, tempfile
        from pathlib import Path
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_mark_allocation.json').read_text())
        base['human_review_required'] = False
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_mark.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='mark_allocation')
        self.assertEqual(d['decision'], 'reject')

    def test_valid_mark_allocation_allow_or_warn(self):
        d = evaluate_file('tests/fixtures/securerails_policy/valid_mark_allocation.json', context_type='mark_allocation')
        self.assertEqual(d['decision'], 'escalate')


if __name__ == '__main__':
    unittest.main()
