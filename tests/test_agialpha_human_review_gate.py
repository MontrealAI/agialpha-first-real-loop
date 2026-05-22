from agialpha_engine.human_review_gate import evaluate_human_review_gate


def test_human_review_gate_defaults_pending_and_blocks_activation():
    result = evaluate_human_review_gate({})
    assert result["human_review_status"] == "pending"
    assert result["outside_sandbox_activation_allowed"] is False


def test_human_review_gate_allows_activation_only_with_all_checks_and_acceptance():
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
    assert result["outside_sandbox_activation_allowed"] is True
