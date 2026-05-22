import unittest

from agialpha_engine.human_review_gate import evaluate_human_review_gate


class TestHumanReviewGate(unittest.TestCase):
    def test_defaults_pending_and_blocks_activation(self) -> None:
        result = evaluate_human_review_gate({})
        self.assertEqual(result["human_review_status"], "pending")
        self.assertFalse(result["outside_sandbox_activation_allowed"])

    def test_allows_activation_only_with_all_checks_and_acceptance(self) -> None:
        result = evaluate_human_review_gate(
            {
                "human_review_status": "accepted",
                "evidence_docket_present": True,
                "proofbundle_present": True,
                "replay_pass": True,
                "falsification_pass": True,
                "claim_boundary_pass": True,
                "token_boundary_pass": True,
                "regulated_boundary_pass": True,
                "no_auto_merge": True,
                "no_autonomous_persistence": True,
            }
        )
        self.assertTrue(result["outside_sandbox_activation_allowed"])

    def test_rejects_non_boolean_false_like_strings(self) -> None:
        result = evaluate_human_review_gate(
            {
                "human_review_status": "accepted",
                "evidence_docket_present": True,
                "proofbundle_present": True,
                "replay_pass": "false",
                "falsification_pass": True,
                "claim_boundary_pass": True,
                "token_boundary_pass": True,
                "regulated_boundary_pass": True,
                "no_auto_merge": True,
                "no_autonomous_persistence": True,
            }
        )
        self.assertFalse(result["outside_sandbox_activation_allowed"])
        self.assertIn("replay_pass", result["missing_or_failed_checks"])
        self.assertIn("replay_pass", result["non_boolean_required_checks"])

    def test_requires_explicit_safety_flags(self) -> None:
        result = evaluate_human_review_gate(
            {
                "human_review_status": "accepted",
                "evidence_docket_present": True,
                "proofbundle_present": True,
                "replay_pass": True,
                "falsification_pass": True,
                "claim_boundary_pass": True,
                "token_boundary_pass": True,
                "regulated_boundary_pass": True,
            }
        )
        self.assertFalse(result["outside_sandbox_activation_allowed"])
        self.assertIn("no_auto_merge", result["missing_or_failed_checks"])
        self.assertIn("no_autonomous_persistence", result["missing_or_failed_checks"])


if __name__ == "__main__":
    unittest.main()
