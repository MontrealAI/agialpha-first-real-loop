"""Computed metrics for measured recursive machine labor proof runs."""
from __future__ import annotations

from typing import Any

MISSING = "not_reported"
UNAVAILABLE = "unavailable"
SAFETY_COUNTERS = [
    "claim_boundary_violations", "token_boundary_violations", "regulated_boundary_violations",
    "raw_secret_leak_count", "external_target_scan_count", "exploit_execution_count",
    "malware_generation_count", "social_engineering_content_count", "unsafe_automerge_count",
    "critical_safety_incidents",
]


def _score(rows: list[dict[str, Any]]) -> float | str:
    if not rows:
        return MISSING
    return round(sum(float(r.get("score", 0.0)) for r in rows) / len(rows), 6)


def compute_metrics(raw: dict[str, Any], min_threshold: float = 0.01) -> dict[str, Any]:
    pairs = raw.get("mandate_pairs", [])
    treatment = raw.get("treatment_results", [])
    shadow = raw.get("shadow_control_results", [])
    treatment_score = _score(treatment)
    shadow_score = _score(shadow)
    if isinstance(treatment_score, float) and isinstance(shadow_score, float):
        delta = round(treatment_score - shadow_score, 6)
        lift = UNAVAILABLE if shadow_score == 0 else round(delta / shadow_score * 100.0, 6)
        vrci = round(delta * len(pairs), 6)
        b6_beats = delta >= min_threshold and treatment_score > shadow_score
    else:
        delta = lift = vrci = b6_beats = MISSING
    metrics = {
        "mandate_pairs_run": len(pairs),
        "mandate_A_tasks": sum(len(p.get("mandate_A", {}).get("training_fixtures", [])) for p in pairs),
        "mandate_B_heldout_tasks": sum(len(p.get("mandate_B", {}).get("heldout_fixtures", [])) for p in pairs),
        "capabilities_generated": len(raw.get("generated_capabilities", [])),
        "capabilities_frozen": len(raw.get("frozen_capabilities", [])),
        "capability_hashes": raw.get("capability_hashes", {}),
        "heldout_leakage_detected": raw.get("heldout_leakage_detected", MISSING),
        "treatment_success_rate": treatment_score,
        "shadow_control_success_rate": shadow_score,
        "treatment_score": treatment_score,
        "shadow_control_score": shadow_score,
        "improvement_delta": delta,
        "improvement_lift_pct": lift,
        "vRCI_computed": vrci,
        "vRCI_formula": "(TreatmentScore_B - ShadowControlScore_B) * mandate_pairs_run",
        "B6_beats_B5_computed": b6_beats,
        "B6_vs_B5_formula": "treatment_score > shadow_control_score and improvement_delta >= configured_minimum_threshold",
        "B4_rejected": raw.get("B4_rejected", MISSING),
        "replay_pass": raw.get("replay_pass", "pending"),
        "falsification_pass": raw.get("falsification_pass", "pending"),
        "proofbundle_complete": raw.get("proofbundle_complete", "pending"),
        "evidence_docket_complete": raw.get("evidence_docket_complete", "pending"),
        "semantic_negative_tests_passed": raw.get("semantic_negative_tests_passed", "pending"),
        "adversarial_fixtures_passed": raw.get("adversarial_fixtures_passed", "pending"),
        "metrics_computed_from_raw_results": bool(treatment and shadow),
        "raw_numerator_denominator": {
            "treatment_rows": len(treatment),
            "control_rows": len(shadow),
            "mandate_pairs": len(pairs),
        },
        "configured_minimum_threshold": min_threshold,
    }
    safety = raw.get("safety_counters", {})
    for key in SAFETY_COUNTERS:
        metrics[key] = safety.get(key, MISSING)
    metrics["stronger_claim_supported"] = stronger_claim_supported(metrics)
    return metrics


def stronger_claim_supported(metrics: dict[str, Any]) -> bool:
    bool_gates = [
        metrics.get("capabilities_frozen", 0) == metrics.get("capabilities_generated", -1) and metrics.get("capabilities_frozen", 0) > 0,
        metrics.get("heldout_leakage_detected") is False,
        isinstance(metrics.get("treatment_score"), (int, float)) and isinstance(metrics.get("shadow_control_score"), (int, float)) and metrics["treatment_score"] > metrics["shadow_control_score"],
        isinstance(metrics.get("improvement_delta"), (int, float)) and metrics["improvement_delta"] >= metrics.get("configured_minimum_threshold", 0.01),
        metrics.get("replay_pass") is True,
        metrics.get("falsification_pass") is True,
        metrics.get("proofbundle_complete") is True,
        metrics.get("evidence_docket_complete") is True,
        metrics.get("B4_rejected") is True,
        metrics.get("metrics_computed_from_raw_results") is True,
        metrics.get("B6_beats_B5_computed") is True,
    ]
    safety_ok = all(metrics.get(k) == 0 for k in SAFETY_COUNTERS)
    return all(bool_gates) and safety_ok


def compute_network_skill_propagation_metrics(
    *,
    heldout_rows_b5: list[dict[str, Any]],
    heldout_rows_b6: list[dict[str, Any]],
    raw_task_result_ids: list[str],
    jobs_run: int = 0,
    jobs_with_skill_extraction: int = 0,
    accepted_skill_packages: int = 0,
    rejected_skill_candidates: int = 0,
    failure_learning_packages: int = 0,
    skills_published_to_vault: int = 0,
    agents_registered: int = 0,
    agent_skill_manifests_created: int | None = None,
    skill_import_events: int = 0,
    target_agents_with_imported_skill: int = 0,
    replay_pass_rate: float | str = "pending",
    falsification_pass: bool | str = "pending",
    semantic_tests_passed: bool | str = "pending",
    safety_counters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute ENGINE-003 network-skill propagation metrics from raw held-out rows.

    This adapter keeps the top-level metrics module useful for Engine-003 while
    delegating the actual D_network and lift formulas to
    :mod:`agialpha_engine.network_skill_metrics`.  It intentionally requires raw
    held-out row references and returns ``not_reported`` for incomplete row
    inputs rather than fabricating zeroes.
    """
    from .network_skill_metrics import compute_network_skill_metrics

    metrics = compute_network_skill_metrics(
        jobs_run=jobs_run,
        jobs_with_skill_extraction=jobs_with_skill_extraction,
        accepted_skill_packages=accepted_skill_packages,
        rejected_skill_candidates=rejected_skill_candidates,
        failure_learning_packages=failure_learning_packages,
        skills_published_to_vault=skills_published_to_vault,
        agents_registered=agents_registered,
        agent_skill_manifests_created=agent_skill_manifests_created,
        skill_import_events=skill_import_events,
        target_agents_with_imported_skill=target_agents_with_imported_skill,
        heldout_rows_b5=heldout_rows_b5,
        heldout_rows_b6=heldout_rows_b6,
        raw_task_result_ids=raw_task_result_ids,
        replay_pass_rate=replay_pass_rate,
        falsification_pass=falsification_pass,
        semantic_tests_passed=semantic_tests_passed,
        safety_counters=safety_counters,
    )
    metrics["metrics_computed_from_raw_logs"] = bool(
        raw_task_result_ids and heldout_rows_b5 and heldout_rows_b6
    )
    return metrics
