from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

from .context import BOUNDARIES

DEFAULT_AGENT_ROLES = ("Reviewer Agent", "Validator Agent", "Operator Agent")


def base_record(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    rec = {**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required": True, "autonomous_persistence_allowed": False, "no_auto_merge": True})
    return rec


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def make_agent(agent_id: str, role: str, *, native_skill_ids: Iterable[str] | None = None) -> dict[str, Any]:
    """Create a deterministic Engine-003 agent registry entry."""
    if not agent_id or not role:
        raise ValueError("agent_id and role are required")
    payload = {
        "schema_version": "agialpha.agent_registry.agent.v1",
        "agent_id": agent_id,
        "role": role,
        "native_skill_ids": sorted(str(s) for s in (native_skill_ids or []) if str(s)),
        "network_imports_allowed": True,
        "production_activation_allowed": False,
        "imported_skills_inactive_outside_sandbox": True,
        **base_record(),
    }
    payload["agent_hash"] = _hash(payload)
    return payload


def register_default_agents(target_agents: int = 3) -> list[dict[str, Any]]:
    """Register at least Reviewer, Validator, and Operator target agents deterministically."""
    count = max(3, int(target_agents))
    roles = list(DEFAULT_AGENT_ROLES) + [f"Sandbox Target Agent {i}" for i in range(4, count + 1)]
    return [make_agent(f"target-agent-{i}", role) for i, role in enumerate(roles[:count], start=1)]


def make_agent_registry(agents: list[dict[str, Any]]) -> dict[str, Any]:
    return base_record({"schema_version": "agialpha.agent_registry.v1", "agents": agents, "agent_count": len(agents)})


__doc__ = "Agent registry helpers for network-compounding runs."
