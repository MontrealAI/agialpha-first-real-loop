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
            with self.assertRaises(ValueError):
                run_lifecycle('.',1,1,0,1,td,candidate_kernel_mutations=0)


    def test_all_opportunities_have_dossiers(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',2,4,2,1,td)
            base=Path(td)/'agiga-foundry-evidence-docket'
            opps=json.loads((base/'04_opportunity_intermediates/opportunities.json').read_text())
            dossiers=json.loads((base/'20_sovereign_opportunity_dossiers/dossiers.json').read_text())
            self.assertEqual(len(dossiers),len(opps))


    def test_heldout_tasks_bind_all_locked_candidate_hashes(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',1,4,2,1,td,candidate_kernel_mutations=3)
            base=Path(td)/'agiga-foundry-evidence-docket'
            lock=json.loads((base/'12_foundry_kernel_rsi/candidate_lock_manifest.json').read_text())
            heldout=json.loads((base/'12_foundry_kernel_rsi/heldout_tasks.json').read_text())
            represented={t['lock_hash'] for t in heldout}
            self.assertEqual(represented,set(lock['candidate_hashes'].values()))


    def test_k5_k6_scores_come_from_heldout_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',1,4,2,1,td,candidate_kernel_mutations=2)
            base=Path(td)/'agiga-foundry-evidence-docket/12_foundry_kernel_rsi'
            summary=json.loads((base/'K5_vs_K6.json').read_text())
            heldout=json.loads((base/'heldout_tasks.json').read_text())
            self.assertEqual(summary['heldout_task_count'], len({t['task_id'] for t in heldout}))
            self.assertEqual(set(summary['candidate_scores'].keys()), set(json.loads((base/'candidate_lock_manifest.json').read_text())['candidate_hashes'].keys()))

    def test_zero_variants_reports_zero_win_rate(self):
        with tempfile.TemporaryDirectory() as td:
            run_lifecycle('.',1,4,2,0,td)
            score=self._score(td)
            self.assertEqual(score['local_variants_generated'],0)
            self.assertEqual(score['local_variant_win_rate'],0.0)

if __name__=='__main__':
    unittest.main()
