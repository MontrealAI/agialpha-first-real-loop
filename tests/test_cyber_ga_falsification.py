import unittest
from pathlib import Path
from agialpha_cyber_ga_sovereign.falsification import run_falsification
from agialpha_cyber_ga_sovereign.lifecycle import run_lifecycle

class T(unittest.TestCase):
    def test_smoke(self):
        out=Path('cyber-ga-sovereign-runs/fals-ok')
        run_lifecycle(Path('.'),1,2,1,1,out)
        result=run_falsification(out/'cyber-ga-sovereign-evidence-docket')
        self.assertEqual(result['status'],'pass')

    def test_fail_when_missing_docket_evidence(self):
        result=run_falsification(Path('cyber-ga-sovereign-runs/missing-fals-docket'))
        self.assertEqual(result['status'],'fail')
