from __future__ import annotations

from typing import Any


THESIS_LINES = (
    "Every Job makes an AI Agent smarter.",
    "Every new skill can be instantly shared across the network.",
    "One Agent learns, all Agents level up.",
)

CAVEAT = (
    "Instant sharing means sandboxed registration and importability. Production "
    "activation requires validators and human review. Exponential compounding is "
    "a strategic target unless the exponential claim gate passes."
)

EXPONENTIAL_BOUNDARY = (
    "Exponential compounding is a strategic target. Current evidence reports "
    "local bounded network skill propagation only."
)

PROOF_CHAIN = (
    "AGI Job → Skill Package / Rejected Skill / Failure Learning → ProofBundle → "
    "Evidence Docket → Network Skill Vault → Agent Skill Manifest → Held-out "
    "Reuse Test → B6 vs B5 → NetworkSkillPropagationLift → Claim Gate → Human Review"
)

FOOTER_DOCTRINE = (
    "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production "
    "is allowed; autonomous claim promotion is not."
)

STATUS_CARD_KEYS = (
    ("jobs run", "jobs_run"),
    ("accepted Skill Packages", "accepted_skill_packages"),
    ("rejected Skill Candidates", "rejected_skill_candidates"),
    ("Failure Learning Packages", "failure_learning_packages"),
    ("skills published", "skills_published_to_vault"),
    ("agents registered", "agents_registered"),
    ("skill imports", "skill_import_events"),
    ("target agents improved", "target_agents_improved_on_heldout"),
    ("held-out tasks evaluated", "heldout_tasks_evaluated"),
    ("B6 beats B5", "B6_shared_skill_beats_B5_no_shared_skill"),
    ("NetworkSkillPropagationLift", "network_skill_propagation_lift"),
    ("CompoundingExponentProxy", "compounding_exponent_proxy"),
    ("exponential compounding supported", "exponential_compounding_supported"),
    ("replay status", "replay_pass_rate"),
    ("falsification status", "falsification_pass"),
)

HARD_SAFETY_KEYS = (
    "raw_secret_leak_count",
    "external_target_scan_count",
    "exploit_execution_count",
    "malware_generation_count",
    "social_engineering_content_count",
    "unsafe_automerge_count",
    "critical_safety_incidents",
)


def _display(value: Any) -> str:
    if value is None:
        return "not_reported"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def render_skill_network_summary(metrics: dict[str, Any], claim_gate: dict[str, Any]) -> str:
    """Render the public-facing Engine-003 summary without promoting unsupported claims."""
    lines = [
        "# AGI ALPHA Skill Network",
        "",
        *THESIS_LINES,
        "",
        "## Caveat",
        CAVEAT,
        "",
        "## Proof chain",
        PROOF_CHAIN,
        "",
        "## Claim gate",
        f"- Claim gate status: {claim_gate.get('claim_gate_status', 'not_supported')}",
        f"- Supported wording: {claim_gate.get('supported_wording', 'Networked skill compounding claim not yet supported.')}",
        "",
        "## Exponential compounding status",
        f"- Status: {metrics.get('exponential_compounding_status', EXPONENTIAL_BOUNDARY)}",
        f"- Supported: {_display(metrics.get('exponential_compounding_supported', False))}",
        "",
        "## Status cards",
    ]
    for label, key in STATUS_CARD_KEYS:
        lines.append(f"- {label}: {_display(metrics.get(key, 'not_reported'))}")
    lines.extend(["", "## Hard safety counters"])
    for key in HARD_SAFETY_KEYS:
        lines.append(f"- {key}: {_display(metrics.get(key, 'not_reported'))}")
    lines.extend([
        "",
        "## Boundary doctrine",
        EXPONENTIAL_BOUNDARY,
        FOOTER_DOCTRINE,
    ])
    return "\n".join(lines)
