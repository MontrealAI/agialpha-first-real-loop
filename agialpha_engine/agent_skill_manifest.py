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


def create_agent_skill_manifest(
    agent_id: str,
    *,
    native_skills: Iterable[str] | None = None,
    imported_skills: Iterable[str] | None = None,
    quarantined_skills: Iterable[str] | None = None,
    rejected_skills: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Create a manifest with imported skills sandbox-inactive by default."""
    if not agent_id:
        raise ValueError("agent_id is required")
    manifest = {
        "schema_version": "agialpha.agent_skill_manifest.v1",
        "agent_id": agent_id,
        "native_skills": sorted(str(s) for s in (native_skills or []) if str(s)),
        "imported_skills": sorted(str(s) for s in (imported_skills or []) if str(s)),
        "quarantined_skills": sorted(str(s) for s in (quarantined_skills or []) if str(s)),
        "rejected_skills": sorted(str(s) for s in (rejected_skills or []) if str(s)),
        "activation_status": "sandbox_registered_inactive_outside_sandbox",
        "production_activation_allowed": False,
        "human_review_status": "pending",
        **base_record(),
    }
    manifest["manifest_hash"] = _hash(manifest)
    return manifest


def add_imported_skill(manifest: dict[str, Any], skill_id: str) -> dict[str, Any]:
    if not skill_id:
        raise ValueError("skill_id is required")
    imported = set(str(s) for s in manifest.get("imported_skills", []) if str(s))
    imported.add(skill_id)
    return create_agent_skill_manifest(
        str(manifest.get("agent_id", "")),
        native_skills=manifest.get("native_skills", []),
        imported_skills=imported,
        quarantined_skills=manifest.get("quarantined_skills", []),
        rejected_skills=manifest.get("rejected_skills", []),
    )


__doc__ = "Agent skill manifest helpers."
