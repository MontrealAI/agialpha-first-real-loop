from __future__ import annotations

from typing import Any


def _constraint_value(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in record:
            return record[key]
    return None


def enforce_equal_budget(control: dict[str, Any], treatment: dict[str, Any]) -> bool:
    control_budget = _constraint_value(control, "budget_units", "budget_proxy")
    treatment_budget = _constraint_value(treatment, "budget_units", "budget_proxy")
    control_validators = _constraint_value(control, "validator_gates", "validator_set")
    treatment_validators = _constraint_value(treatment, "validator_gates", "validator_set")
    return (
        control_budget is not None
        and treatment_budget is not None
        and control_validators is not None
        and treatment_validators is not None
        and control_budget == treatment_budget
        and control_validators == treatment_validators
    )


def _coerce_score(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def compute_delta(control: dict[str, Any], treatment: dict[str, Any]) -> dict[str, Any]:
    if not enforce_equal_budget(control, treatment):
        return {"status": "blocked", "reason": "unequal_constraints"}
    c = _coerce_score(control.get("score"))
    t = _coerce_score(treatment.get("score"))
    if c is None or t is None:
        return {"status": "blocked", "reason": "missing_or_invalid_score"}
    return {"status": "ok", "delta": round(t - c, 6), "treatment_wins": t > c}
