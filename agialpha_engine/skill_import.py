from __future__ import annotations

import hashlib
import json
from typing import Any

from .context import BOUNDARIES


def base_record(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True})
    return rec


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def create_skill_import_event(import_id: str, skill_package: dict[str, Any], target_agent_id: str) -> dict[str, Any]:
    """Record a sandbox-only import, quarantining incomplete skill evidence."""
    skill_id = skill_package.get("skill_id")
    has_evidence = bool(skill_package.get("proofbundle_id") and skill_package.get("evidence_docket_id") and skill_package.get("raw_task_result_ids"))
    status = "imported_inactive_outside_sandbox" if has_evidence else "quarantined_missing_evidence"
    activation_status = "inactive" if has_evidence else "quarantined"
    event = {
        "schema_version": "agialpha.skill_import.v1",
        "import_id": import_id,
        "skill_id": skill_id,
        "target_agent_id": target_agent_id,
        "import_status": status,
        "activation_status": activation_status,
        "active_outside_sandbox": False,
        "production_activation_allowed": False,
        "quarantine_reason": "" if has_evidence else "missing ProofBundle, Evidence Docket, or raw task result ids",
        "proofbundle_id": skill_package.get("proofbundle_id") or "unavailable",
        "evidence_docket_id": skill_package.get("evidence_docket_id") or "unavailable",
        **base_record(),
    }
    event["skill_import_hash"] = _hash(event)
    return event


__doc__ = "Skill import event helpers."
