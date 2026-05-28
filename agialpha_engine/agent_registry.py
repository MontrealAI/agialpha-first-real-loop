from __future__ import annotations

import hashlib
import json
from typing import Iterable

from .context import BOUNDARIES

DEFAULT_AGENT_ROLES = ("Reviewer Agent", "Validator Agent", "Operator Agent")


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


def stable_agent_id(role: str, seed: int) -> str:
    digest = hashlib.sha256(f"{seed}:{role}".encode("utf-8")).hexdigest()[:10]
    slug = role.lower().replace(" ", "-")
    return f"agent-{slug}-{digest}"


def build_agent_registry(target_agents: int, seed: int, roles: Iterable[str] | None = None) -> list[dict]:
    """Build deterministic sandbox-only target agents for skill import tests."""
    selected_roles = list(roles or DEFAULT_AGENT_ROLES)
    if target_agents > len(selected_roles):
        selected_roles.extend(f"Auxiliary Agent {idx}" for idx in range(len(selected_roles) + 1, target_agents + 1))
    agents: list[dict] = []
    for idx, role in enumerate(selected_roles[:target_agents], start=1):
        agent = base_record({
            "schema_version": "agialpha.engine.agent_registry.v1",
            "agent_id": stable_agent_id(role, seed),
            "agent_name": role,
            "role": role,
            "ordinal": idx,
            "sandbox_only": True,
            "production_activation_allowed": False,
            "network_calls_allowed": False,
        })
        agent["agent_hash"] = hashlib.sha256(json.dumps(agent, sort_keys=True).encode("utf-8")).hexdigest()
        agents.append(agent)
    return agents


__all__ = ["DEFAULT_AGENT_ROLES", "base_record", "stable_agent_id", "build_agent_registry"]
