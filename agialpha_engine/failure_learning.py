from __future__ import annotations

import hashlib
import json

from .context import BOUNDARIES


def base_record(extra=None):
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
        "no_auto_merge": True,
    })
    return rec


def build_failure_learning(job_id: str, reason: str, *, raw_task_result_ids: list[str] | None = None) -> dict:
    package = base_record({
        "schema_version": "agialpha.engine.failure_learning_package.v1",
        "failure_learning_id": f"fl-{hashlib.sha256(job_id.encode()).hexdigest()[:12]}",
        "source_job_id": job_id,
        "raw_task_result_ids": raw_task_result_ids or [],
        "reason": reason,
        "learning_type": "failure_warning",
        "reusable_learning": "Preserve the failure mode for future tests, quarantine, or harder validation.",
        "activation_status": "inactive",
        "production_activation_allowed": False,
    })
    package["failure_learning_hash"] = hashlib.sha256(json.dumps(package, sort_keys=True).encode("utf-8")).hexdigest()
    return package


def build_rejected_skill_candidate(job_id: str, reason: str, *, raw_task_result_ids: list[str] | None = None) -> dict:
    candidate = base_record({
        "schema_version": "agialpha.engine.rejected_skill_candidate.v1",
        "rejected_skill_candidate_id": f"rsc-{hashlib.sha256((job_id + reason).encode()).hexdigest()[:12]}",
        "source_job_id": job_id,
        "raw_task_result_ids": raw_task_result_ids or [],
        "rejected_reason": reason,
        "quarantined": True,
        "activation_status": "inactive",
        "production_activation_allowed": False,
    })
    candidate["rejected_skill_candidate_hash"] = hashlib.sha256(json.dumps(candidate, sort_keys=True).encode("utf-8")).hexdigest()
    return candidate


__all__ = ["base_record", "build_failure_learning", "build_rejected_skill_candidate"]
