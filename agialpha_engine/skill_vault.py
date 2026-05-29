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


def publish_skill_package(skill_package: dict[str, Any]) -> dict[str, Any]:
    """Create an append-only Network Skill Vault entry for a proof-bound skill."""
    skill_id = skill_package.get("skill_id")
    raw_ids = skill_package.get("raw_task_result_ids", [])
    if not skill_id:
        raise ValueError("skill package must include skill_id")
    if not raw_ids:
        raise ValueError(f"skill package {skill_id} must reference raw_task_result_ids")
    if not skill_package.get("proofbundle_id") or not skill_package.get("evidence_docket_id"):
        raise ValueError(f"skill package {skill_id} must include ProofBundle and Evidence Docket ids")
    entry = {
        "schema_version": "agialpha.network_skill_vault_entry.v1",
        "skill_id": skill_id,
        "skill_package_hash": _hash(skill_package),
        "published": True,
        "activation_status": "sandbox_registered_inactive_outside_sandbox",
        "allowed_import_scope": skill_package.get("allowed_import_scope", "sandbox_only"),
        "proofbundle_id": skill_package.get("proofbundle_id"),
        "evidence_docket_id": skill_package.get("evidence_docket_id"),
        "raw_task_result_ids": list(raw_ids),
        **base_record(),
    }
    entry["vault_entry_hash"] = _hash(entry)
    return entry


def make_vault(skill_packages: list[dict[str, Any]]) -> dict[str, Any]:
    entries = [publish_skill_package(skill) for skill in skill_packages]
    return base_record({"schema_version": "agialpha.network_skill_vault.v1", "skill_packages": skill_packages, "vault_entries": entries, "skill_count": len(entries)})


__doc__ = "Sandbox vault publication helpers."
