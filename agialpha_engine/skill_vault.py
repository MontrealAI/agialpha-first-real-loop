from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

from .context import BOUNDARIES


def base_record(extra=None):
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True})
    return rec


def _hash_payload(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def publish_skill_packages_to_vault(*, run_id: str, skill_packages: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Publish accepted proof-bound skills to the local Network Skill Vault index."""
    entries = []
    for package in skill_packages:
        entry = base_record(
            {
                "schema_version": "agialpha.network_skill_vault.entry.v1",
                "run_id": run_id,
                "skill_id": package.get("skill_id"),
                "source_job_id": package.get("source_job_id"),
                "source_agent_id": package.get("source_agent_id"),
                "proofbundle_id": package.get("proofbundle_id"),
                "evidence_docket_id": package.get("evidence_docket_id"),
                "allowed_import_scope": package.get("allowed_import_scope", "sandbox_only"),
                "activation_status": "inactive_outside_sandbox",
                "published": bool(package.get("skill_id") and package.get("proofbundle_id") and package.get("evidence_docket_id")),
            }
        )
        entry["vault_entry_hash"] = _hash_payload(entry)
        entries.append(entry)
    return base_record({"schema_version": "agialpha.network_skill_vault.v1", "run_id": run_id, "skill_packages": entries})


__doc__ = "Sandbox vault publication helpers."
