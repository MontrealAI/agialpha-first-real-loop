from __future__ import annotations

import hashlib
import json

from .context import BOUNDARIES
from .skill_package import evidence_id_present


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


def build_skill_import_event(*, skill_id: str, source_agent_id: str, target_agent_id: str, proofbundle_id: str | None, evidence_docket_id: str | None, seed: int) -> dict:
    has_evidence = evidence_id_present(proofbundle_id) and evidence_id_present(evidence_docket_id)
    status = "imported" if has_evidence else "quarantined_missing_evidence"
    event = base_record({
        "schema_version": "agialpha.engine.skill_import.v1",
        "skill_import_id": f"import-{hashlib.sha256(f'{seed}:{skill_id}:{target_agent_id}'.encode()).hexdigest()[:12]}",
        "skill_id": skill_id,
        "source_agent_id": source_agent_id,
        "target_agent_id": target_agent_id,
        "proofbundle_id": proofbundle_id,
        "evidence_docket_id": evidence_docket_id,
        "import_status": status,
        "activation_status": "inactive",
        "allowed_import_scope": "sandbox_only",
        "production_activation_allowed": False,
        "poisoned_skill_quarantined": not has_evidence,
    })
    event["skill_import_hash"] = hashlib.sha256(json.dumps(event, sort_keys=True).encode("utf-8")).hexdigest()
    return event


__all__ = ["base_record", "build_skill_import_event"]
