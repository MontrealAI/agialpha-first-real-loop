import unittest
from pathlib import Path
import json
from agialpha_cyber_ga_sovereign.lifecycle import run_lifecycle

class T(unittest.TestCase):
    def test_generate(self):
        out=Path('cyber-ga-sovereign-runs/test-unit')
        run_lifecycle(Path('.'),1,16,6,3,out)
        self.assertTrue((out/'cyber-ga-sovereign-evidence-docket/evidence-run-manifest.json').exists())

    def test_cycles_honored(self):
        out=Path('cyber-ga-sovereign-runs/test-cycles')
        run_lifecycle(Path('.'),2,4,2,3,out)
        metrics=json.loads((out/'cyber-ga-sovereign-evidence-docket/28_summary_tables/scoreboard.json').read_text())['metrics']
        self.assertEqual(metrics['cycles_executed'],2)
        self.assertEqual(metrics['candidate_defensive_niches_generated'],8)
