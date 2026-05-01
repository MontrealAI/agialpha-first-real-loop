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


if __name__ == '__main__':
    unittest.main()
