import json
import tempfile
import unittest
from pathlib import Path
from secure_rails.policy_kernel import evaluate_file


class TestSecureRailsPolicySovereign(unittest.TestCase):
    def test_valid_sovereign_allow_or_warn(self):
        d = evaluate_file('tests/fixtures/securerails_policy/valid_sovereign.json', context_type='sovereign')
        self.assertIn(d['decision'], {'allow', 'warn'})

    def test_sovereign_with_automerge_rejected(self):
        base = json.loads(Path('tests/fixtures/securerails_policy/valid_sovereign.json').read_text())
        base['auto_merge_allowed'] = True
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad.json'
            p.write_text(json.dumps(base), encoding='utf-8')
            d = evaluate_file(str(p), context_type='sovereign')
        self.assertEqual(d['decision'], 'reject')


if __name__ == '__main__':
    unittest.main()
