"""Safe PR planning helpers for RSI-GOVERNOR-001."""

from __future__ import annotations

from .promotion import promotion_gate


def prepare_safe_pr_plan(metrics: dict) -> dict:
    """Prepare safe-PR decision artifact without creating or merging a PR."""
    decision = promotion_gate(metrics)
    return {
        "open_pr": bool(decision.get("pass")),
        "automerge": False,
        "promotion_gate": decision,
        "required_title": "RSI-GOVERNOR-001: propose executable governance-kernel promotion",
    }


__all__ = ["prepare_safe_pr_plan"]
