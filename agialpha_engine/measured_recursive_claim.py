"""Measured recursive claim decision utility."""
from __future__ import annotations
from typing import Any

ALLOWED_CLAIM = "In this local repo-owned benchmark, AGI ALPHA demonstrated machine labor that recursively improves in a measured, falsifiable way."


def decide_claim(metrics: dict[str, Any], conditions: dict[str, bool]) -> dict[str, Any]:
    blocked = [k for k, v in conditions.items() if v is not True]
    status = "supported" if not blocked and metrics.get("stronger_claim_supported") is True else "blocked"
    return {
        "claim": ALLOWED_CLAIM,
        "status": status,
        "blocked_reasons": blocked,
        "allowed_public_wording": ALLOWED_CLAIM if status == "supported" else "Not demonstrated yet.",
    }
