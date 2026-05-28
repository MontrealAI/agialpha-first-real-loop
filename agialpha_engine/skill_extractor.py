from __future__ import annotations

from .context import BOUNDARIES
from .failure_learning import build_failure_learning, build_rejected_skill_candidate
from .skill_package import build_skill_package


def base_record(extra=None):
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True})
    return rec


def classify_job(job_index: int) -> str:
    return ["accepted", "rejected", "failure"][job_index % 3]


def extract_learning_from_job(job: dict, raw_result: dict, job_index: int) -> dict:
    """Deterministically route each job into reusable accepted/rejected/failure learning."""
    outcome = classify_job(job_index)
    job_id = job["job_id"]
    raw_ids = [raw_result["task_result_id"]]
    if outcome == "accepted" and raw_result.get("passed") is True:
        return {"outcome": outcome, "record": build_skill_package(
            source_job_id=job_id,
            source_agent_id=job.get("agent_id", raw_result.get("agent_id", "source-agent")),
            skill_type="capability_package",
            skill_payload={"portable_capability": job.get("task_family", "local evidence repair"), "sandbox_only": True},
            raw_task_result_ids=raw_ids,
        )}
    if outcome == "rejected":
        return {"outcome": outcome, "record": build_rejected_skill_candidate(job_id, "validator margin insufficient for publication", raw_task_result_ids=raw_ids)}
    return {"outcome": "failure", "record": build_failure_learning(job_id, raw_result.get("failure_reason") or "held for harder regression testing", raw_task_result_ids=raw_ids)}


__all__ = ["base_record", "classify_job", "extract_learning_from_job"]
