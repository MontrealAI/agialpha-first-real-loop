"""Regulated-boundary triage for Ascension OS enterprise workflows."""

from __future__ import annotations

REGULATED_FLAGS = [
    "financial advice",
    "investment advice",
    "payment/custody",
    "wallet/trading",
    "KYC/AML",
    "legal advice",
    "medical advice",
    "HR/worker evaluation",
    "credit/lending",
    "insurance",
    "critical-infrastructure control",
    "energy/utility markets",
    "biometric identification",
    "emotion recognition",
    "law enforcement",
    "migration/border",
    "education access/scoring",
    "justice/democratic process",
    "offensive cyber",
]


def _keywords(flag: str) -> list[str]:
    return [part.strip().lower() for part in flag.split("/") if part.strip()]


def regulated_boundary_triage(workflow: dict) -> dict:
    text = f"{workflow.get('workflow_type', '')} {workflow.get('description', '')}".lower()
    hits = [flag for flag in REGULATED_FLAGS if any(term in text for term in _keywords(flag))]
    blocked = bool(hits)
    return {
        "regulated_flags_triggered": hits,
        "regulated_boundary_blocked": blocked,
        "status": "blocked_human_review_required" if blocked else "documentation_only",
        "safe_explanation": (
            "No automated execution for regulated domains; documentation-only handoff required."
            if blocked
            else "Synthetic non-regulated workflow."
        ),
        "human_review_required": True,
    }
