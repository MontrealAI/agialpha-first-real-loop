import unittest, tempfile, json
from pathlib import Path
from agialpha_agiga_foundry.lifecycle import run_lifecycle

class T(unittest.TestCase):
    def _score(self, td):
        return json.loads((Path(td)/'agiga-foundry-evidence-docket/22_summary_tables/scoreboard.json').read_text())

    def test_cycles_affect_generation_count(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',2,4,2,1,td)
            score=self._score(td)
            self.assertEqual(score['candidate_niches_generated'],8)
            self.assertEqual(score['candidate_niches_evaluated'],4)

    def test_zero_evaluated_niches_does_not_crash(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',1,4,0,1,td)
            score=self._score(td)
            self.assertEqual(score['candidate_niches_evaluated'],0)
            self.assertEqual(score['solved_niches'],0)

    def test_evaluated_count_is_capped_by_generated(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',2,3,9,1,td)
            score=self._score(td)
            self.assertEqual(score['candidate_niches_evaluated'],6)

    def test_opportunity_ids_unique_across_cycles(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',3,4,2,1,td)
            opps=json.loads((Path(td)/'agiga-foundry-evidence-docket/04_opportunity_intermediates/opportunities.json').read_text())
            ids=[o['opportunity_id'] for o in opps]
            self.assertEqual(len(ids),len(set(ids)))


    def test_negative_inputs_fail_fast(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                run_lifecycle('.',1,-1,0,1,td)
            with self.assertRaises(ValueError):
                run_lifecycle('.',1,1,-1,1,td)
            with self.assertRaises(ValueError):
                run_lifecycle('.',1,1,0,-1,td)

if __name__=='__main__':
    unittest.main()
