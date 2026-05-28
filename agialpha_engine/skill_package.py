from __future__ import annotations

import hashlib
import json
from typing import Any

from .context import BOUNDARIES

SKILL_TYPES = {
    "validator", "workflow_template", "scoring_rubric", "safety_rule", "replay_recipe",
    "redaction_rule", "claim_boundary_rule", "token_boundary_rule", "regulated_boundary_rule",
    "test_fixture", "operator_wrapper", "failure_warning", "capability_package",
}


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


def stable_skill_id(source_job_id: str, source_agent_id: str, skill_type: str) -> str:
    digest = hashlib.sha256(f"{source_job_id}:{source_agent_id}:{skill_type}".encode("utf-8")).hexdigest()[:12]
    return f"skill-{digest}"


MISSING_EVIDENCE_IDS = {"", "pending", "not_reported", "unavailable", "skipped_with_reason"}


def evidence_id_present(value: Any) -> bool:
    """Return True only for concrete evidence identifiers, not placeholders."""
    if value is None:
        return False
    text = str(value).strip()
    return bool(text) and text.lower() not in MISSING_EVIDENCE_IDS


def build_skill_package(*, source_job_id: str, source_agent_id: str, skill_type: str, skill_payload: dict[str, Any], raw_task_result_ids: list[str], proofbundle_id: str = "pending", evidence_docket_id: str = "pending") -> dict[str, Any]:
    if skill_type not in SKILL_TYPES:
        raise ValueError(f"unsupported skill_type: {skill_type}")
    if not raw_task_result_ids:
        raise ValueError("accepted skill packages require raw_task_result_ids")
    skill_id = stable_skill_id(source_job_id, source_agent_id, skill_type)
    package = base_record({
        "schema_version": "agialpha.engine.skill_package.v1",
        "skill_id": skill_id,
        "source_job_id": source_job_id,
        "source_agent_id": source_agent_id,
        "skill_type": skill_type,
        "skill_payload": skill_payload,
        "validated_on_task_ids": list(raw_task_result_ids),
        "raw_task_result_ids": list(raw_task_result_ids),
        "proofbundle_id": proofbundle_id,
        "evidence_docket_id": evidence_docket_id,
        "replay_status": "pass" if evidence_id_present(proofbundle_id) else "pending",
        "falsification_status": "pass" if evidence_id_present(evidence_docket_id) else "pending",
        "risk_tier": "low",
        "allowed_import_scope": "sandbox_only",
        "activation_policy": "inactive_outside_sandbox_until_human_review",
        "production_activation_allowed": False,
    })
    package["skill_hash"] = hashlib.sha256(json.dumps(package, sort_keys=True).encode("utf-8")).hexdigest()
    return package


def has_required_evidence(package: dict[str, Any]) -> bool:
    return (
        bool(package.get("raw_task_result_ids"))
        and evidence_id_present(package.get("proofbundle_id"))
        and evidence_id_present(package.get("evidence_docket_id"))
    )


__all__ = [
    "SKILL_TYPES",
    "base_record",
    "stable_skill_id",
    "evidence_id_present",
    "build_skill_package",
    "has_required_evidence",
]
