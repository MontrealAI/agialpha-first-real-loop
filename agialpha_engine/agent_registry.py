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


def deterministic_agent_id(role: str, index: int) -> str:
    """Return a stable local-only target-agent identifier for a network run."""
    slug = "-".join(str(role).strip().lower().split()) or "agent"
    return f"agent-{index:02d}-{slug}"


def build_agent_record(*, agent_id: str, role: str, run_id: str, seed: int, sandbox_only: bool = True) -> dict[str, Any]:
    """Build one bounded Agent Registry row.

    Agents registered by Engine-003 are deterministic local actors used for
    sandboxed import/reuse tests; they are not autonomous production agents.
    """
    record = base_record(
        {
            "schema_version": "agialpha.agent_registry.v1",
            "agent_id": agent_id,
            "role": role,
            "run_id": run_id,
            "seed": seed,
            "sandbox_only": sandbox_only,
            "production_activation_allowed": False,
            "native_skill_ids": [],
            "imported_skill_ids": [],
        }
    )
    record["agent_hash"] = _hash_payload(record)
    return record


def build_agent_registry(*, run_id: str, roles: Iterable[str], seed: int) -> dict[str, Any]:
    """Build a deterministic registry for target agents participating in import tests."""
    agents = [
        build_agent_record(agent_id=deterministic_agent_id(role, index), role=role, run_id=run_id, seed=seed + index)
        for index, role in enumerate(roles, start=1)
    ]
    return base_record({"schema_version": "agialpha.agent_registry.index.v1", "run_id": run_id, "agents": agents})


__doc__ = "Agent registry helpers for network-compounding runs."
