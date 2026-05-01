import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestRsiGovernorAutonomyContract(unittest.TestCase):
    def test_operator_required_actions_must_be_list(self):
        base = json.loads(Path('config/rsi_governor_autonomy_contract.json').read_text())
        base['operator_required_actions'] = 'run_replay'
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad-contract.json'
            p.write_text(json.dumps(base))
            proc = subprocess.run(
                ['python', '-m', 'agialpha_rsi_governor', 'validate-autonomy-contract', '--contract', str(p)],
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('invalid operator_required_actions', proc.stderr + proc.stdout)

    def test_forbidden_action_rejected_in_autonomous_pre(self):
        base = json.loads(Path('config/rsi_governor_autonomy_contract.json').read_text())
        base['autonomous_pre_promotion_actions'] = list(base['autonomous_pre_promotion_actions']) + ['merge_pr']
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad-contract-forbidden.json'
            p.write_text(json.dumps(base))
            proc = subprocess.run(
                ['python', '-m', 'agialpha_rsi_governor', 'validate-autonomy-contract', '--contract', str(p)],
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('forbidden autonomous actions present', proc.stderr + proc.stdout)

    def test_cannot_bypass_with_empty_forbidden_list(self):
        base = json.loads(Path('config/rsi_governor_autonomy_contract.json').read_text())
        base['forbidden_autonomous_actions'] = []
        base['autonomous_pre_promotion_actions'] = list(base['autonomous_pre_promotion_actions']) + ['merge_pr']
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad-contract-empty-forbidden.json'
            p.write_text(json.dumps(base))
            proc = subprocess.run(
                ['python', '-m', 'agialpha_rsi_governor', 'validate-autonomy-contract', '--contract', str(p)],
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('contract missing required forbidden_autonomous_actions policy entries', proc.stderr + proc.stdout)


if __name__ == '__main__':
    unittest.main()
