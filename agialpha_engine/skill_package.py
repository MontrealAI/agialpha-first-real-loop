from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .context import BOUNDARIES

_PENDING_STATUS = "pending"
_ALLOWED_AUDIT_STATUSES = {_PENDING_STATUS, "pass", "fail"}
_PLACEHOLDER_EVIDENCE_IDS = {"", "pending", "placeholder", "none", "null", "n/a", "na"}


def base_record(extra=None):
    rec={**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True})
    return rec


def evidence_id_present(evidence_id: str | None) -> bool:
    """Return whether an evidence identifier is a non-placeholder value."""
    if evidence_id is None:
        return False
    return str(evidence_id).strip().lower() not in _PLACEHOLDER_EVIDENCE_IDS


def _list(value: Iterable[str] | None) -> list[str]:
    if value is None:
        return []
    return list(value)


def _audit_status(name: str, value: str) -> str:
    if value not in _ALLOWED_AUDIT_STATUSES:
        allowed = ", ".join(sorted(_ALLOWED_AUDIT_STATUSES))
        raise ValueError(f"{name} must be one of: {allowed}")
    return value


def create_skill_package(
    *,
    skill_id: str,
    source_job_id: str,
    source_agent_id: str,
    skill_type: str = "workflow_template",
    skill_payload: dict[str, Any] | None = None,
    validated_on_task_ids: Iterable[str] | None = None,
    raw_task_result_ids: Iterable[str] | None = None,
    proofbundle_id: str | None = None,
    evidence_docket_id: str | None = None,
    replay_status: str = _PENDING_STATUS,
    falsification_status: str = _PENDING_STATUS,
    risk_tier: str = "low",
    allowed_import_scope: str = "sandbox_only",
    activation_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a skill package without converting evidence IDs into audit pass states.

    ProofBundle and Evidence Docket identifiers only prove that artifacts were assigned.
    Replay and falsification must remain pending until the dedicated audit workflows
    write explicit pass/fail statuses.
    """
    if activation_policy is None:
        activation_policy = {
            "auto_activate_allowed": False,
            "human_review_required": True,
            "validator_required": True,
            "replay_required": True,
            "falsification_required": True,
        }

    return base_record(
        {
            "schema_version": "agialpha.skill_package.v1",
            "skill_id": skill_id,
            "source_job_id": source_job_id,
            "source_agent_id": source_agent_id,
            "skill_type": skill_type,
            "skill_payload": skill_payload or {},
            "validated_on_task_ids": _list(validated_on_task_ids),
            "raw_task_result_ids": _list(raw_task_result_ids),
            "proofbundle_id": proofbundle_id,
            "proofbundle_id_present": evidence_id_present(proofbundle_id),
            "evidence_docket_id": evidence_docket_id,
            "evidence_docket_id_present": evidence_id_present(evidence_docket_id),
            "replay_status": _audit_status("replay_status", replay_status),
            "falsification_status": _audit_status("falsification_status", falsification_status),
            "risk_tier": risk_tier,
            "allowed_import_scope": allowed_import_scope,
            "activation_policy": activation_policy,
        }
    )


__doc__ = "Skill package creation helpers."
