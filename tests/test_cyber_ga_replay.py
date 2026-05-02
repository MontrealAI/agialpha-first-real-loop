import unittest
from pathlib import Path
from agialpha_cyber_ga_sovereign.replay import run_replay
from agialpha_cyber_ga_sovereign.lifecycle import run_lifecycle

class T(unittest.TestCase):
    def test_smoke(self):
        out=Path('cyber-ga-sovereign-runs/replay-ok')
        run_lifecycle(Path('.'),1,2,1,1,out)
        result=run_replay(out/'cyber-ga-sovereign-evidence-docket')
        self.assertEqual(result['status'],'pass')

    def test_fail_when_missing_docket_evidence(self):
        result=run_replay(Path('cyber-ga-sovereign-runs/missing-docket'))
        self.assertEqual(result['status'],'fail')
