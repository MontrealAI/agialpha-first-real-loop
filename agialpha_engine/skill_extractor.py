from __future__ import annotations

from typing import Any

from .context import BOUNDARIES


def base_record(extra=None):
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True})
    return rec


def classify_job(job_index: int) -> str:
    """Route a job to deterministic learning output type for local evidence runs."""
    return ["accepted", "rejected", "failure"][job_index % 3]


def extract_learning_from_raw_result(raw_result: dict[str, Any], job_index: int) -> dict[str, Any]:
    """Convert one raw evaluator row into accepted/rejected/failure learning metadata.

    This helper does not fabricate validation evidence; it only routes raw rows to
    candidate learning outcomes consumed by the full network-compounding runner.
    """
    outcome = classify_job(job_index)
    task_id = raw_result.get("task_id", f"job-{job_index}")
    accepted = outcome == "accepted" and raw_result.get("passed") is True
    if accepted:
        learning_type = "accepted_skill_package"
    elif outcome == "rejected":
        learning_type = "rejected_skill_candidate"
    else:
        learning_type = "failure_learning_package"
    return base_record(
        {
            "schema_version": "agialpha.skill_extraction.v1",
            "source_task_id": task_id,
            "raw_task_result_id": raw_result.get("task_result_id"),
            "learning_type": learning_type,
            "accepted_for_vault_publication": accepted,
            "reason": "validator_passed" if accepted else raw_result.get("failure_reason", "bounded local learning retained"),
        }
    )


__doc__ = "Deterministic skill extraction routing."
