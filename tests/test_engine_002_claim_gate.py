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
