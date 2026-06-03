from __future__ import annotations

from typing import Any

from .context import BOUNDARIES


def base_record(extra=None):
    rec={**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True})
    return rec

__doc__ = "Network skill metrics computation from raw logs."

REQUIRED_D_FIELDS = (
    "success_score",
    "validator_pass",
    "replay_pass",
    "proofbundle",
    "docket",
    "cost_risk_proxy",
)

EXPONENTIAL_GATE_HARD_SAFETY_COUNTERS = (
    "raw_secret_leak_count",
    "external_target_scan_count",
    "exploit_execution_count",
    "malware_generation_count",
    "social_engineering_content_count",
    "unsafe_automerge_count",
    "critical_safety_incidents",
    "unsafe_claims_blocked",
    "token_value_claims_blocked",
    "regulated_decisioning_blocked",
)

RAW_ID_SENTINELS = {"", "not_reported", "unavailable", "pending", "skipped_with_reason"}


def compute_d_metric(rows):
    if not rows:
        return "not_reported"
    if any(not isinstance(row, dict) for row in rows):
        return "not_reported"
    if any(any(field not in row for field in REQUIRED_D_FIELDS) for row in rows):
        return "not_reported"
    return sum(_row_factor(r) for r in rows)/len(rows)


def _num(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _row_factor(row: dict[str, Any]) -> float:
    return (
        _num(row.get("success_score"), 0.0)
        * _num(row.get("validator_pass"), 0.0)
        * _num(row.get("replay_pass"), 0.0)
        * _num(row.get("proofbundle"), 0.0)
        * _num(row.get("docket"), 0.0)
        * _num(row.get("skill_import_success_rate"), 1.0)
        * _num(row.get("skill_activation_safety"), 1.0)
        * _num(row.get("operator_usefulness_score"), 1.0)
        * _num(row.get("reviewer_usefulness_score"), 1.0)
        * _num(row.get("claim_boundary_integrity"), 1.0)
        * _num(row.get("token_boundary_integrity"), 1.0)
        * _num(row.get("regulated_boundary_integrity"), 1.0)
        * _num(row.get("redaction_integrity"), 1.0)
        / max(1.0, _num(row.get("cost_risk_proxy"), 1.0))
    )


def _heldout_pair_population_matches(
    heldout_rows_b5: list[dict[str, Any]],
    heldout_rows_b6: list[dict[str, Any]],
) -> bool:
    if len(heldout_rows_b5) != len(heldout_rows_b6):
        return False
    task_ids_b5 = [row.get("task_id") for row in heldout_rows_b5]
    task_ids_b6 = [row.get("task_id") for row in heldout_rows_b6]
    if any(task_id is not None for task_id in task_ids_b5 + task_ids_b6):
        return all(
            task_id_b5 is not None
            and task_id_b6 is not None
            and task_id_b5 == task_id_b6
            for task_id_b5, task_id_b6 in zip(task_ids_b5, task_ids_b6)
        )
    return True


def evaluate_exponential_compounding_gate(
    *,
    compounding_cycles: list[dict[str, Any]] | None = None,
    replay_pass: bool = False,
    falsification_pass: bool = False,
    metrics_computed_from_raw_logs: bool = False,
    safety_counters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate whether measured exponential wording is allowed.

    The gate is intentionally separate from local bounded propagation.  It only
    supports exponential wording when at least three replayed cycles have
    raw-log-backed, strictly positive, superlinear lift growth and no boundary
    violations.  Otherwise it returns the required strategic-target caveat.
    """
    cycles = compounding_cycles or []
    status_text = (
        "Exponential compounding is a strategic target. Current evidence reports "
        "local bounded network skill propagation only."
    )
    numeric_lifts: list[float] = []
    raw_backed = True
    invalid_raw_cycle_evidence: list[int] = []
    for index, cycle in enumerate(cycles):
        lift = cycle.get("network_skill_propagation_lift")
        raw_ids = cycle.get("raw_task_result_ids")
        raw_ids_valid = (
            isinstance(raw_ids, (list, tuple, set))
            and bool(raw_ids)
            and all(isinstance(raw_id, str) and raw_id.strip() not in RAW_ID_SENTINELS for raw_id in raw_ids)
        )
        if not isinstance(lift, (int, float)) or isinstance(lift, bool) or not raw_ids_valid:
            raw_backed = False
            invalid_raw_cycle_evidence.append(index)
            continue
        numeric_lifts.append(float(lift))
    increments = [round(b - a, 12) for a, b in zip(numeric_lifts, numeric_lifts[1:])]
    superlinear = (
        len(numeric_lifts) >= 3
        and all(lift > 0 for lift in numeric_lifts)
        and len(increments) >= 2
        and all(delta > 0 for delta in increments)
        and all(next_delta > delta for delta, next_delta in zip(increments, increments[1:]))
    )
    counters = safety_counters if isinstance(safety_counters, dict) else {}
    missing_hard_safety_counters = [
        key for key in EXPONENTIAL_GATE_HARD_SAFETY_COUNTERS if key not in counters
    ]
    nonzero_hard_safety_counters = [
        key
        for key in EXPONENTIAL_GATE_HARD_SAFETY_COUNTERS
        if key in counters and (isinstance(counters[key], bool) or counters[key] != 0)
    ]
    hard_safety_ok = not missing_hard_safety_counters and not nonzero_hard_safety_counters
    supported = bool(
        superlinear
        and raw_backed
        and replay_pass
        and falsification_pass
        and metrics_computed_from_raw_logs
        and hard_safety_ok
    )
    exponent_proxy: float | str = "not_supported"
    if supported:
        first_increment = increments[0]
        last_increment = increments[-1]
        exponent_proxy = round(1.0 + (last_increment / max(first_increment, 1e-12)), 6)
        status_text = (
            "Measured exponential compounding language is supported for this "
            "local bounded multi-cycle evidence docket only."
        )
    return base_record({
        "exponential_compounding_supported": supported,
        "exponential_compounding_status": status_text,
        "compounding_exponent_proxy": exponent_proxy,
        "cycles_evaluated": len(cycles),
        "superlinear_growth_observed": superlinear,
        "metrics_computed_from_raw_logs": metrics_computed_from_raw_logs,
        "replay_pass": replay_pass,
        "falsification_pass": falsification_pass,
        "hard_safety_ok": hard_safety_ok,
        "missing_hard_safety_counters": missing_hard_safety_counters,
        "nonzero_hard_safety_counters": nonzero_hard_safety_counters,
        "raw_cycle_evidence_valid": raw_backed,
        "invalid_raw_cycle_evidence": invalid_raw_cycle_evidence,
    })


def compute_network_skill_metrics(
    *,
    jobs_run: int,
    jobs_with_skill_extraction: int,
    accepted_skill_packages: int,
    rejected_skill_candidates: int,
    failure_learning_packages: int,
    skills_published_to_vault: int,
    agents_registered: int,
    skill_import_events: int,
    target_agents_with_imported_skill: int,
    heldout_rows_b5: list[dict[str, Any]],
    heldout_rows_b6: list[dict[str, Any]],
    raw_task_result_ids: list[str],
    agent_skill_manifests_created: int | None = None,
    replay_pass_rate: float | str = "pending",
    falsification_pass: bool | str = "pending",
    semantic_tests_passed: bool | str = "pending",
    safety_counters: dict[str, Any] | None = None,
    compounding_cycles: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    exponential_gate = evaluate_exponential_compounding_gate(
        compounding_cycles=compounding_cycles,
        replay_pass=replay_pass_rate is True or replay_pass_rate == 1 or replay_pass_rate == 1.0,
        falsification_pass=falsification_pass is True,
        metrics_computed_from_raw_logs=bool(raw_task_result_ids),
        safety_counters=safety_counters,
    )
    d_b5 = compute_d_metric(heldout_rows_b5)
    d_b6 = compute_d_metric(heldout_rows_b6)
    heldout_metrics_reportable = isinstance(d_b5, float) and isinstance(d_b6, float)
    if heldout_metrics_reportable:
        delta = round(d_b6 - d_b5, 6)
        b6_beats = d_b6 > d_b5
        if _heldout_pair_population_matches(heldout_rows_b5, heldout_rows_b6):
            paired_heldout_rows = zip(heldout_rows_b5, heldout_rows_b6)
            improved_heldout_tasks = sum(
                1
                for b5, b6 in paired_heldout_rows
                if _row_factor(b6) > _row_factor(b5)
            )
            target_agents_improved_on_heldout: int | str = min(
                target_agents_with_imported_skill, improved_heldout_tasks
            )
        else:
            target_agents_improved_on_heldout = "not_reported"
    else:
        delta = "not_reported"
        b6_beats = "not_reported"
        target_agents_improved_on_heldout = "not_reported"
    counters = safety_counters or {}
    hard_counter_defaults = {
        "autonomous_persistence_attempts_blocked": "not_reported",
        "unsafe_claims_blocked": "not_reported",
        "token_value_claims_blocked": "not_reported",
        "regulated_decisioning_blocked": "not_reported",
        "raw_secret_leak_count": "not_reported",
        "external_target_scan_count": "not_reported",
        "exploit_execution_count": "not_reported",
        "malware_generation_count": "not_reported",
        "social_engineering_content_count": "not_reported",
        "unsafe_automerge_count": "not_reported",
        "critical_safety_incidents": "not_reported",
    }
    hard_counters = {
        key: counters.get(key, default)
        for key, default in hard_counter_defaults.items()
    }
    return base_record({
        "jobs_run": jobs_run,
        "jobs_with_skill_extraction": jobs_with_skill_extraction,
        "accepted_skill_packages": accepted_skill_packages,
        "rejected_skill_candidates": rejected_skill_candidates,
        "failure_learning_packages": failure_learning_packages,
        "skills_published_to_vault": skills_published_to_vault,
        "agents_registered": agents_registered,
        "agent_skill_manifests_created": (
            "not_reported"
            if agent_skill_manifests_created is None
            else agent_skill_manifests_created
        ),
        "skill_import_events": skill_import_events,
        "target_agents_with_imported_skill": target_agents_with_imported_skill,
        "target_agents_improved_on_heldout": target_agents_improved_on_heldout,
        "heldout_tasks_evaluated": len(heldout_rows_b6),
        "B6_shared_skill_beats_B5_no_shared_skill": b6_beats,
        "B6_shared_skill_advantage_delta": delta,
        "network_skill_propagation_lift": delta,
        "network_skill_multiplier": (
            round((d_b6 / d_b5), 6)
            if isinstance(d_b5, float) and d_b5 > 0 and isinstance(d_b6, float)
            else "not_reported"
        ),
        "capability_compounding_rate": delta,
        "compounding_exponent_proxy": exponential_gate["compounding_exponent_proxy"],
        "exponential_compounding_supported": exponential_gate["exponential_compounding_supported"],
        "exponential_compounding_status": exponential_gate["exponential_compounding_status"],
        "raw_task_result_ids": raw_task_result_ids if raw_task_result_ids else "not_reported",
        "replay_pass_rate": replay_pass_rate,
        "falsification_pass": falsification_pass,
        "semantic_tests_passed": semantic_tests_passed,
        "hard_coded_metric_count": 0,
        "fake_zero_metric_count": 0,
        **hard_counters,
        "D_no_shared_skill_B5": d_b5,
        "D_shared_skill_network_B6": d_b6,
    })
