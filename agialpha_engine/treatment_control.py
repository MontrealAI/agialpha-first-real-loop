from __future__ import annotations

from typing import Any


def enforce_equal_budget(control: dict[str, Any], treatment: dict[str, Any]) -> bool:
    return control.get("budget_proxy") == treatment.get("budget_proxy") and control.get("validator_set") == treatment.get("validator_set")


def compute_delta(control: dict[str, Any], treatment: dict[str, Any]) -> dict[str, Any]:
    if not enforce_equal_budget(control, treatment):
        return {"status": "blocked", "reason": "unequal_constraints"}
    c = float(control.get("score", 0.0))
    t = float(treatment.get("score", 0.0))
    return {"status": "ok", "delta": round(t - c, 6), "treatment_wins": t > c}
