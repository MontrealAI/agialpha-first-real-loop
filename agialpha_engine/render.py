from __future__ import annotations

from typing import Any


def render_skill_network_summary(metrics: dict[str, Any], claim_gate: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# AGI ALPHA Skill Network",
            "",
            "Every Job makes an AI Agent smarter.",
            "Every new skill can be instantly shared across the network.",
            "One Agent learns, all Agents level up.",
            "",
            f"- jobs run: {metrics.get('jobs_run', 'not_reported')}",
            f"- accepted Skill Packages: {metrics.get('accepted_skill_packages', 'not_reported')}",
            f"- rejected Skill Candidates: {metrics.get('rejected_skill_candidates', 'not_reported')}",
            f"- Failure Learning Packages: {metrics.get('failure_learning_packages', 'not_reported')}",
            f"- NetworkSkillPropagationLift: {metrics.get('network_skill_propagation_lift', 'not_reported')}",
            f"- Claim gate status: {claim_gate.get('claim_gate_status', 'not_supported')}",
            "",
            "Exponential compounding is a strategic target. Current evidence reports local bounded networked skill propagation only.",
        ]
    )
