from agialpha_engine.network_claim_gate import evaluate_network_compounding_claim
from secure_rails.human_review import validate_promotion_gate


def _supported_kwargs():
    return dict(
        jobs_run=5,
        exact_one_outcome_per_job=True,
        accepted_skill_packages=1,
        distinct_import_targets=3,
        d_shared_skill_network=0.75,
        d_no_shared_skill=0.70,
        replay_ok=True,
        falsification_ok=True,
        critical_safety_incidents=0,
        proofbundle_present=True,
        evidence_docket_present=True,
        skill_published_to_vault=True,
        imports_inactive_outside_sandbox=True,
        heldout_test_ran=True,
        metrics_computed_from_raw_logs=True,
        hard_safety_invariants_zero=True,
        no_token_or_investment_overclaim=True,
        no_regulated_decisioning=True,
        no_autonomous_persistence=True,
        human_review_required_outside_sandbox=True,
    )


def test_network_claim_gate_blocks_missing_proofbundle_and_docket():
    kwargs = _supported_kwargs()
    kwargs["proofbundle_present"] = False
    kwargs["evidence_docket_present"] = False
    gate = evaluate_network_compounding_claim(**kwargs)
    assert gate["claim_gate_status"] == "not_supported"
    assert "accepted_skill_has_proofbundle" in gate["failed_reasons"]
    assert "accepted_skill_has_evidence_docket" in gate["failed_reasons"]


def test_network_claim_gate_blocks_production_active_imports_and_non_raw_metrics():
    kwargs = _supported_kwargs()
    kwargs["imports_inactive_outside_sandbox"] = False
    kwargs["metrics_computed_from_raw_logs"] = False
    gate = evaluate_network_compounding_claim(**kwargs)
    assert gate["claim_gate_status"] == "not_supported"
    assert "imports_inactive_outside_sandbox" in gate["failed_reasons"]
    assert "metrics_computed_from_raw_logs" in gate["failed_reasons"]


def test_securerails_promotion_gate_defaults_to_pending_human_review():
    errors = validate_promotion_gate(
        {
            "schema_version": "securerails.promotion_gate.v1",
            "promotion_gate_id": "gate-001",
            "source_decision_id": "decision-001",
            "promotion_target": "safe_pr",
            "required_conditions": {
                "human_review_decision_present": True,
                "hard_safety_counters_zero": True,
                "auto_merge_allowed": False,
                "evidence_docket_present": True,
            },
            "claim_boundary": "No Evidence Docket, no empirical SOTA claim.",
        }
    )
    assert "promotion pending human review" in errors
