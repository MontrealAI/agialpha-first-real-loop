"""Safe PR planning helpers for RSI-GOVERNOR-001."""

from __future__ import annotations

from .promotion import MINIMUM_ADVANTAGE_DELTA, promotion_gate


def prepare_safe_pr_plan(metrics: dict) -> dict:
    """Prepare safe-PR decision artifact without creating or merging a PR."""
    delta = float(metrics.get("B6_advantage_delta_vs_B5", 0.0))
    eci = str(metrics.get("ECI_level", ""))
    passes = promotion_gate(delta, eci, minimum_advantage_delta=MINIMUM_ADVANTAGE_DELTA)
    return {
        "open_pr": passes,
        "automerge": False,
        "promotion_gate": {
            "pass": passes,
            "delta": delta,
            "eci": eci,
            "minimum_advantage_delta": MINIMUM_ADVANTAGE_DELTA,
            "minimum_eci_for_promotion": "E3_REPLAYED",
        },
        "required_title": "RSI-GOVERNOR-001: propose executable governance-kernel promotion",
    }


__all__ = ["prepare_safe_pr_plan"]
