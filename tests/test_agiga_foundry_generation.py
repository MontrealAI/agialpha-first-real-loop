import unittest, tempfile, json
from pathlib import Path
from agialpha_agiga_foundry.lifecycle import run_lifecycle

class T(unittest.TestCase):
    def test_cycles_affect_generation_count(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',2,4,2,1,td)
            score=json.loads((Path(td)/'agiga-foundry-evidence-docket/22_summary_tables/scoreboard.json').read_text())
            self.assertEqual(score['candidate_niches_generated'],8)
            self.assertEqual(score['candidate_niches_evaluated'],4)

    def test_zero_evaluated_niches_does_not_crash(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',1,4,0,1,td)
            score=json.loads((Path(td)/'agiga-foundry-evidence-docket/22_summary_tables/scoreboard.json').read_text())
            self.assertEqual(score['candidate_niches_evaluated'],0)
            self.assertEqual(score['solved_niches'],0)

if __name__=='__main__':
    unittest.main()
