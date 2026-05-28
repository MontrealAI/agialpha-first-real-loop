from __future__ import annotations

import hashlib
import json
from typing import Iterable

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


def build_manifest(agent: dict, native_skills: Iterable[str] | None = None) -> dict:
    manifest = base_record({
        "schema_version": "agialpha.engine.agent_skill_manifest.v1",
        "agent_id": agent["agent_id"],
        "agent_name": agent.get("agent_name", agent.get("role", "unknown")),
        "native_skills": sorted(set(native_skills or [])),
        "imported_skills": [],
        "quarantined_skills": [],
        "rejected_skills": [],
        "skill_import_policy": {
            "default_activation_status": "inactive",
            "outside_sandbox_activation_requires_human_review": True,
            "proofbundle_required": True,
            "evidence_docket_required": True,
            "regulated_domain_import_policy": "quarantine",
        },
        "activation_status": "sandbox_importable_only",
        "production_activation_allowed": False,
    })
    manifest["manifest_hash"] = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
    return manifest


def import_skill_into_manifest(manifest: dict, skill_id: str, *, proofbundle_id: str, evidence_docket_id: str) -> dict:
    updated = json.loads(json.dumps(manifest, sort_keys=True))
    if not (evidence_id_present(proofbundle_id) and evidence_id_present(evidence_docket_id)):
        updated.setdefault("quarantined_skills", []).append(skill_id)
    elif skill_id not in updated.setdefault("imported_skills", []):
        updated["imported_skills"].append(skill_id)
        updated["imported_skills"].sort()
    updated["activation_status"] = "sandbox_importable_only"
    updated["production_activation_allowed"] = False
    updated["manifest_hash"] = hashlib.sha256(json.dumps({k: v for k, v in updated.items() if k != "manifest_hash"}, sort_keys=True).encode("utf-8")).hexdigest()
    return updated


__all__ = ["base_record", "build_manifest", "import_skill_into_manifest"]
