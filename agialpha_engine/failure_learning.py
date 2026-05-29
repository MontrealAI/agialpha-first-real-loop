from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

from .context import BOUNDARIES


def base_record(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True})
    return rec


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def build_failure_learning(
    job_id: str,
    reason: str,
    *,
    source_agent_id: str = "agent-1",
    raw_task_result_ids: Iterable[str] | None = None,
    failure_category: str = "validator_or_replay_learning",
) -> dict[str, Any]:
    """Preserve reusable learning for a job that should not become an active skill."""
    if not job_id or not reason:
        raise ValueError("job_id and reason are required")
    ids = list(raw_task_result_ids or [f"raw-{job_id}"])
    package = {
        "schema_version": "agialpha.failure_learning_package.v1",
        "failure_learning_id": f"fl-{job_id}",
        "source_job_id": job_id,
        "source_agent_id": source_agent_id,
        "failure_category": failure_category,
        "failure_summary": reason,
        "reason": reason,
        "raw_task_result_ids": ids,
        "reuse_policy": "test_harder_before_activation",
        "activation_status": "not_active_failure_learning_only",
        **base_record(),
    }
    package["failure_learning_hash"] = _hash(package)
    return package


__doc__ = "Failure learning package helpers."
