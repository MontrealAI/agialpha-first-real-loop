from __future__ import annotations

import hashlib
import json
from typing import Iterable

from .context import BOUNDARIES
from .skill_package import has_required_evidence


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


def publish_to_vault(skill_packages: Iterable[dict]) -> dict:
    """Create an append-only vault view that refuses evidence-free accepted skills."""
    entries = []
    rejected = []
    for package in skill_packages:
        if has_required_evidence(package):
            entry = base_record({
                "schema_version": "agialpha.engine.network_skill_vault_entry.v1",
                "skill_id": package["skill_id"],
                "source_job_id": package.get("source_job_id"),
                "source_agent_id": package.get("source_agent_id"),
                "proofbundle_id": package.get("proofbundle_id"),
                "evidence_docket_id": package.get("evidence_docket_id"),
                "publication_status": "published_sandbox_importable",
                "activation_status": "inactive",
                "production_activation_allowed": False,
            })
            entry["vault_entry_hash"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode("utf-8")).hexdigest()
            entries.append(entry)
        else:
            rejected.append(base_record({
                "skill_id": package.get("skill_id", "unknown"),
                "publication_status": "rejected_missing_proofbundle_or_evidence_docket",
                "quarantined": True,
            }))
    return base_record({
        "schema_version": "agialpha.engine.network_skill_vault.v1",
        "skill_packages": entries,
        "rejected_publications": rejected,
        "append_only": True,
        "skills_published_to_vault": len(entries),
    })


__all__ = ["base_record", "publish_to_vault"]
