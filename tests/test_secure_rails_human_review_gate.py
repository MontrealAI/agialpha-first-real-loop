import unittest
from secure_rails.human_review import validate_promotion_gate


def _record(decision: str):
    return {
        "schema_version": "securerails.promotion_gate.v1",
        "promotion_gate_id": "pg-1",
        "source_decision_id": "d-1",
        "promotion_target": "safe_pr",
        "required_conditions": {
            "human_review_decision_present": True,
            "hard_safety_counters_zero": True,
            "auto_merge_allowed": False,
            "evidence_docket_present": True,
        },
        "human_review": {"decision": decision},
        "claim_boundary": "bounded",
    }


class TestSecureRailsHumanReviewGate(unittest.TestCase):
    def test_accepted_is_required_for_promotion(self):
        self.assertEqual(validate_promotion_gate(_record("accepted")), [])

    def test_rejected_or_needs_changes_block_promotion(self):
        self.assertTrue(validate_promotion_gate(_record("rejected")))
        self.assertTrue(validate_promotion_gate(_record("needs_changes")))

