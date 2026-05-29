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


def create_agent_skill_manifest(
    *,
    agent_id: str,
    native_skills: Iterable[str] | None = None,
    imported_skills: Iterable[dict[str, Any]] | None = None,
    quarantined_skills: Iterable[dict[str, Any]] | None = None,
    rejected_skills: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create a manifest with imported skills inactive outside sandbox by default."""
    manifest = base_record(
        {
            "schema_version": "agialpha.agent_skill_manifest.v1",
            "agent_id": agent_id,
            "native_skills": list(native_skills or []),
            "imported_skills": list(imported_skills or []),
            "quarantined_skills": list(quarantined_skills or []),
            "rejected_skills": list(rejected_skills or []),
            "default_activation_status": "inactive_outside_sandbox",
            "production_activation_allowed": False,
        }
    )
    manifest["manifest_hash"] = _hash_payload(manifest)
    return manifest


def import_skill_into_manifest(manifest: dict[str, Any], skill_id: str, import_event_id: str) -> dict[str, Any]:
    """Return a new manifest row reflecting a sandbox-only skill import."""
    updated = dict(manifest)
    imported = list(updated.get("imported_skills", []))
    imported.append(
        {
            "skill_id": skill_id,
            "import_event_id": import_event_id,
            "activation_status": "inactive",
            "outside_sandbox_activation_allowed": False,
            "human_review_status": "pending",
        }
    )
    updated["imported_skills"] = imported
    updated["production_activation_allowed"] = False
    updated["manifest_hash"] = _hash_payload({k: v for k, v in updated.items() if k != "manifest_hash"})
    return updated


__doc__ = "Agent skill manifest helpers."
