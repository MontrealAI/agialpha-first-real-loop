import json
import tempfile
import unittest
from pathlib import Path
from secure_rails.policy_kernel import evaluate_file


class TestSecureRailsPolicySovereign(unittest.TestCase):
    def test_valid_sovereign_allow_or_warn(self):
        d = evaluate_file('tests/fixtures/securerails_policy/valid_sovereign.json', context_type='sovereign')
        self.assertEqual(d['decision'], 'escalate')


    def test_sovereign_autonomous_promotion_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_sovereign.json').read_text())
        base['promotion_policy'] = {'autonomous_promotion_allowed': True, 'human_review_required': True, 'auto_merge_allowed': False}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_promotion.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertEqual(d['decision'], 'reject')




    def test_sovereign_empty_promotion_policy_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_sovereign.json').read_text())
        base['promotion_policy'] = {}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_empty_policy.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertEqual(d['decision'], 'reject')

    def test_sovereign_string_promotion_flags_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_sovereign.json').read_text())
        base['promotion_policy'] = {'autonomous_promotion_allowed': 'false', 'human_review_required': 'true', 'auto_merge_allowed': 'false'}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_string_flags.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertEqual(d['decision'], 'reject')

    def test_sovereign_required_terms_text_only_bypass_rejected(self):
        obj = {
            'note': 'allowed_work forbidden_work validators proofbundle_policy evidence_docket_policy promotion_policy claim_boundary'
        }
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'text_bypass.json'
            p.write_text(json.dumps(obj), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertEqual(d['decision'], 'reject')

    def test_sovereign_object_autonomous_promotion_flag_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_sovereign.json').read_text())
        base['promotion_policy'] = {'autonomous_promotion_allowed': True, 'human_review_required': True, 'auto_merge_allowed': False}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_object_promotion.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertEqual(d['decision'], 'reject')

    def test_sovereign_human_review_false_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_sovereign.json').read_text())
        base['promotion_policy']['human_review_required'] = False
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad_human_review.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertEqual(d['decision'], 'reject')

    def test_sovereign_negated_autonomous_promotion_text_not_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_sovereign.json').read_text())
        base['claim_boundary'] = 'Autonomous promotion is not allowed; governance remains human reviewed.'
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'negated_text.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertNotEqual(d['decision'], 'reject')

    def test_sovereign_with_automerge_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_sovereign.json').read_text())
        base['promotion_policy']['auto_merge_allowed'] = True
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertEqual(d['decision'], 'reject')


if __name__ == '__main__':
    unittest.main()
