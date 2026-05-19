import unittest
from secure_rails.human_review import validate_promotion_gate

class TestHumanReviewGate002(unittest.TestCase):
    def test_missing_human_review_fails(self):
        rec={"schema_version":"securerails.promotion_gate.v1","promotion_gate_id":"x","source_decision_id":"d","promotion_target":"safe_pr","required_conditions":{"human_review_decision_present":False,"hard_safety_counters_zero":True,"auto_merge_allowed":False,"evidence_docket_present":True},"claim_boundary":"ok"}
        errs=validate_promotion_gate(rec)
        self.assertTrue(any('human_review_decision_present' in e for e in errs))
