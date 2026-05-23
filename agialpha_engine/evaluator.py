"""Evaluator utilities for empirical task results."""
from __future__ import annotations

from typing import Any
from .context import BOUNDARIES
from .sandbox import artifact_hash


def build_task_result(*, task_id: str, candidate_id: str, baseline_id: str, seed: int, sandbox_record: dict[str, Any], validator_results: list[dict[str, Any]], raw_scores: dict[str, Any], cost_proxy: float = 0.0, safety_counters: dict[str, Any] | None = None, source_logs: list[str] | None = None) -> dict[str, Any]:
    safety_counters = safety_counters or {}
    source_logs = source_logs or []
    passed = all(bool(v.get("pass")) for v in validator_results) and sandbox_record.get("status") != "blocked"
    record = {
        "task_result_id": f"task-result-{task_id}-{candidate_id}-{seed}",
        "task_id": task_id,
        "candidate_id": candidate_id,
        "baseline_id": baseline_id,
        "seed": int(seed),
        "sandbox_id": sandbox_record.get("sandbox_id", "unknown"),
        "validator_results": validator_results,
        "raw_scores": raw_scores,
        "cost_proxy": float(cost_proxy),
        "safety_counters": safety_counters,
        "artifact_hashes": {
            "sandbox_record_hash": artifact_hash(sandbox_record),
            "validator_results_hash": artifact_hash(validator_results),
            "raw_scores_hash": artifact_hash(raw_scores),
        },
        "passed": bool(passed),
        "failure_reason": "" if passed else "validator_or_sandbox_failure",
        "claim_boundary": BOUNDARIES["claim_boundary"],
        "source_logs": list(source_logs),
        **BOUNDARIES,
    }
    return record
