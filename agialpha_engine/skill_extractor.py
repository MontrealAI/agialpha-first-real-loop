from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

from .context import BOUNDARIES
from .failure_learning import build_failure_learning
from .skill_package import create_skill_package


_ACCEPTED_TYPES = (
    "validator",
    "workflow_template",
    "scoring_rubric",
    "safety_rule",
    "replay_recipe",
    "redaction_rule",
    "claim_boundary_rule",
    "token_boundary_rule",
    "regulated_boundary_rule",
    "test_fixture",
    "operator_wrapper",
    "failure_warning",
    "capability_package",
)


def base_record(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True})
    return rec


__doc__ = "Deterministic skill extraction routing for ENGINE-003 jobs."


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def classify_job(job_index: int) -> str:
    """Deterministically route demo jobs across accepted/rejected/failure learning buckets."""
    return ["accepted", "rejected", "failure"][job_index % 3]


def _raw_id(raw_task_result: dict[str, Any]) -> str:
    return str(raw_task_result.get("raw_task_result_id") or raw_task_result.get("task_result_id") or "")


def _job_id(raw_task_result: dict[str, Any]) -> str:
    return str(raw_task_result.get("task_id") or raw_task_result.get("job_id") or "")


def _agent_id(raw_task_result: dict[str, Any]) -> str:
    return str(raw_task_result.get("agent_id") or raw_task_result.get("source_agent_id") or "agent-1")


def extract_job_learning(
    raw_task_result: dict[str, Any],
    *,
    job_index: int = 0,
    proofbundle_id: str | None = None,
    evidence_docket_id: str | None = None,
    force_outcome: str | None = None,
) -> dict[str, Any]:
    """Convert one raw evaluator log into exactly one reusable-learning artifact.

    The extractor never drops a job.  Passing jobs assigned to the accepted bucket
    become sandbox-only Skill Packages only when raw task evidence exists and
    evidence identifiers are supplied.  Otherwise the job is preserved as either a
    rejected Skill Candidate or a Failure Learning Package with boundary fields.
    """
    if not isinstance(raw_task_result, dict):
        raise TypeError("raw_task_result must be a dict")
    job_id = _job_id(raw_task_result)
    raw_id = _raw_id(raw_task_result)
    if not job_id or not raw_id:
        raise ValueError("raw_task_result must include task_id/job_id and raw_task_result_id/task_result_id")

    outcome = force_outcome or classify_job(job_index)
    if outcome not in {"accepted", "rejected", "failure"}:
        raise ValueError("force_outcome must be accepted, rejected, or failure")

    passed = raw_task_result.get("passed") is True and all(
        bool(row.get("pass")) for row in raw_task_result.get("validator_results", []) if isinstance(row, dict)
    )
    source_agent_id = _agent_id(raw_task_result)

    if outcome == "accepted" and passed and proofbundle_id and evidence_docket_id:
        artifact = create_skill_package(
            skill_id=f"skill-{job_id.split('-')[-1]}",
            source_job_id=job_id,
            source_agent_id=source_agent_id,
            skill_type="workflow_template",
            skill_payload={"template": "safe_replay_template", "source_raw_task_result_id": raw_id},
            validated_on_task_ids=[job_id],
            raw_task_result_ids=[raw_id],
            proofbundle_id=proofbundle_id,
            evidence_docket_id=evidence_docket_id,
        )
        return {"outcome": "accepted", "artifact": artifact, **base_record()}

    if outcome == "failure" or not passed:
        artifact = build_failure_learning(
            job_id,
            raw_task_result.get("failure_reason") or "validator evidence requires harder replay before activation",
            source_agent_id=source_agent_id,
            raw_task_result_ids=[raw_id],
        )
        return {"outcome": "failure", "artifact": artifact, **base_record()}

    artifact = base_record(
        {
            "schema_version": "agialpha.rejected_skill_candidate.v1",
            "candidate_id": str(raw_task_result.get("candidate_id") or f"cand-{job_id}"),
            "source_job_id": job_id,
            "source_agent_id": source_agent_id,
            "rejection_reason": "accepted_skill_requires_validator_replay_proofbundle_and_evidence_docket",
            "quarantine_required": True,
            "raw_task_result_ids": [raw_id],
            "activation_status": "rejected_not_active",
        }
    )
    artifact["rejected_skill_candidate_hash"] = _hash(artifact)
    return {"outcome": "rejected", "artifact": artifact, **base_record()}


def extract_many_job_learnings(raw_task_results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Extract reusable learning for a sequence of raw task results."""
    rows = list(raw_task_results)
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        result = extract_job_learning(
            row,
            job_index=index,
            proofbundle_id=f"pb-skill-{index + 1}",
            evidence_docket_id=f"ed-skill-{index + 1}",
        )
        if result["outcome"] == "accepted":
            accepted.append(result["artifact"])
        elif result["outcome"] == "rejected":
            rejected.append(result["artifact"])
        else:
            failures.append(result["artifact"])
    produced_jobs = {row.get("source_job_id") for row in accepted + rejected + failures}
    return base_record(
        {
            "schema_version": "agialpha.skill_extraction_report.v1",
            "accepted_skill_packages": accepted,
            "rejected_skill_candidates": rejected,
            "failure_learning_packages": failures,
            "jobs_with_reusable_learning": len(produced_jobs),
            "every_job_produced_reusable_learning": len(produced_jobs) == len(rows),
            "allowed_skill_types": list(_ACCEPTED_TYPES),
        }
    )
