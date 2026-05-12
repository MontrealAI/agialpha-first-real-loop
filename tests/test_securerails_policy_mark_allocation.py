import json
import tempfile
import unittest
from pathlib import Path
from secure_rails.policy_kernel import evaluate_file


class TestSecureRailsPolicyMarkAllocation(unittest.TestCase):
    def test_invalid_mark_automerge_rejected(self):
        d = evaluate_file('tests/fixtures/securerails_policy/invalid_mark_automerge.json', context_type='mark_allocation')
        self.assertEqual(d['decision'], 'reject')

    def test_mark_human_review_false_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_mark_allocation.json').read_text())
        base['human_review_required'] = False
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_human_review.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='mark_allocation')
        self.assertEqual(d['decision'], 'reject')



    def test_mark_string_flag_values_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_mark_allocation.json').read_text())
        base['human_review_required'] = 'true'
        base['proof_required'] = 'true'
        base['promotion_without_evidence_allowed'] = 'false'
        base['auto_merge_allowed'] = 'false'
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_string_flags.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='mark_allocation')
        self.assertEqual(d['decision'], 'reject')

    def test_mark_numeric_flag_values_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_mark_allocation.json').read_text())
        base['human_review_required'] = 1
        base['proof_required'] = 1
        base['promotion_without_evidence_allowed'] = 0
        base['auto_merge_allowed'] = 0
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_numeric_flags.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='mark_allocation')
        self.assertEqual(d['decision'], 'reject')

    def test_mark_required_terms_text_only_bypass_rejected(self):
        obj = {
            'note': 'assigned_sovereign validators_required human_review_required proof_required promotion_without_evidence_allowed auto_merge_allowed claim_boundary'
        }
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'text_bypass.json'
            p.write_text(json.dumps(obj), encoding='utf-8')
            d = evaluate_file(str(p), context_type='mark_allocation')
        self.assertEqual(d['decision'], 'reject')

    def test_mark_negated_automerge_text_not_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_mark_allocation.json').read_text())
        base['claim_boundary'] = 'Auto merge allowed is not allowed; human review required remains true.'
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'negated_text.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='mark_allocation')
        self.assertNotEqual(d['decision'], 'reject')

    def test_valid_mark_allocation_allow_or_warn(self):
        d = evaluate_file('tests/fixtures/securerails_policy/valid_mark_allocation.json', context_type='mark_allocation')
        self.assertEqual(d['decision'], 'escalate')


if __name__ == '__main__':
    unittest.main()
