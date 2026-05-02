import unittest
from pathlib import Path
from agialpha_cyber_ga_sovereign.lifecycle import run_lifecycle
class T(unittest.TestCase):
    def test_generate(self):
        out=Path('cyber-ga-sovereign-runs/test-unit')
        run_lifecycle(Path('.'),1,16,6,3,out)
        self.assertTrue((out/'cyber-ga-sovereign-evidence-docket/evidence-run-manifest.json').exists())
