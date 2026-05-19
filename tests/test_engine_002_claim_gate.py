import json, tempfile, unittest
from pathlib import Path
from agialpha_engine.claim_gate import RecursiveMachineLaborClaimGate

class TestEngine002ClaimGate(unittest.TestCase):
    def test_not_supported_when_missing(self):
        with tempfile.TemporaryDirectory() as td:
            run=Path(td); (run/'06_metrics').mkdir()
            (run/'06_metrics/computed_metrics.json').write_text(json.dumps({}))
            out=RecursiveMachineLaborClaimGate.evaluate(run)
            self.assertEqual(out['status'],'not_supported')
            self.assertTrue(out['failed_requirements'])


    def test_numeric_vrci_counts_as_computed(self):
        with tempfile.TemporaryDirectory() as td:
            run=Path(td); (run/'06_metrics').mkdir()
            metrics={
                'adjacent_mandates_completed':3,
                'frozen_capability_packages_created':1,
                'm2_b6_beats_b5':True,
                'm3_b6_beats_b5':True,
                'B6_beats_B5':True,
                'heldout_descendant_mandates_evaluated':1,
                'replay_passes':1,
                'falsification_pass':True,
                'adversarial_fixtures_generated':1,
                'adversarial_fixtures_caught':1,
                'rejected_variants_preserved':1,
                'human_review_required_count':1,
                'unsafe_automerge_count':0,
                'critical_safety_incidents':0,
                'vRCI_computed':0.25,
                'metrics_computed_from_raw_results':True,
                'hardcoded_metric_markers_found':0,
                'raw_metric_sources':['a.json'],
            }
            (run/'06_metrics/computed_metrics.json').write_text(json.dumps(metrics))
            out=RecursiveMachineLaborClaimGate.evaluate(run)
            self.assertTrue(out['computed_not_hardcoded'])
