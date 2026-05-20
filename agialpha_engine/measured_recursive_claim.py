from __future__ import annotations

from typing import Any

ALLOWED_CLAIM = "In this local repo-owned benchmark, AGI ALPHA demonstrated machine labor that recursively improves in a measured, falsifiable way."
NOT_DEMONSTRATED = "Not demonstrated yet."


def claim_status_from_gate(gate: dict[str, Any]) -> dict[str, Any]:
    status = gate.get("status", "blocked")
    supported = status == "supported"
    return {
        "status": status,
        "supported": supported,
        "public_text": ALLOWED_CLAIM if supported else NOT_DEMONSTRATED,
    }
