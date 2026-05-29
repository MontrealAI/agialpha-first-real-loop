from __future__ import annotations

import hashlib
import json
from typing import Any

from .context import BOUNDARIES


def base_record(extra=None):
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True})
    return rec


def _hash_payload(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def create_skill_import_event(*, run_id: str, skill_package: dict[str, Any], target_agent_id: str, seed: int) -> dict[str, Any]:
    """Create a deterministic import event, rejecting packages without evidence IDs."""
    skill_id = str(skill_package.get("skill_id", ""))
    proofbundle_id = skill_package.get("proofbundle_id")
    evidence_docket_id = skill_package.get("evidence_docket_id")
    accepted = bool(skill_id and proofbundle_id and evidence_docket_id)
    event = base_record(
        {
            "schema_version": "agialpha.skill_import.v1",
            "run_id": run_id,
            "skill_import_id": f"import-{run_id}-{target_agent_id}-{skill_id}",
            "skill_id": skill_id,
            "target_agent_id": target_agent_id,
            "seed": seed,
            "import_status": "accepted" if accepted else "quarantined",
            "activation_status": "inactive",
            "outside_sandbox_activation_allowed": False,
            "quarantine_reason": "" if accepted else "missing ProofBundle or Evidence Docket",
            "proofbundle_id": proofbundle_id,
            "evidence_docket_id": evidence_docket_id,
        }
    )
    event["skill_import_hash"] = _hash_payload(event)
    return event


__doc__ = "Skill import event helpers."
