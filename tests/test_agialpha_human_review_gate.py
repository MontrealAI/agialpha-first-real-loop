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


def test_human_review_gate_rejects_non_boolean_false_like_strings():
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
    assert result["outside_sandbox_activation_allowed"] is False
    assert "replay_pass" in result["missing_or_failed_checks"]
    assert "replay_pass" in result["non_boolean_required_checks"]


def test_human_review_gate_requires_explicit_safety_flags():
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
    assert result["outside_sandbox_activation_allowed"] is False
    assert "no_auto_merge" in result["missing_or_failed_checks"]
    assert "no_autonomous_persistence" in result["missing_or_failed_checks"]
