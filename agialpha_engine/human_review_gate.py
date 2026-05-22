from __future__ import annotations

from typing import Any


VALID_HUMAN_REVIEW_STATUSES = {"pending", "accepted", "needs_changes", "rejected"}
REQUIRED_CHECK_FIELDS = (
    "evidence_docket_present",
    "proofbundle_present",
    "replay_pass",
    "falsification_pass",
    "claim_boundary_pass",
    "token_boundary_pass",
    "regulated_boundary_pass",
    "no_auto_merge",
    "no_autonomous_persistence",
)


def _parse_strict_bool(rec: dict[str, Any], field_name: str) -> tuple[bool, bool]:
    """Return (value, strict_bool_type) for a required gate field."""
    value = rec.get(field_name)
    if isinstance(value, bool):
        return value, True
    return False, False


def evaluate_human_review_gate(record: dict[str, Any] | None) -> dict[str, Any]:
    """Evaluate local human-review requirements for sandbox-to-production activation."""
    rec = record or {}
    status = str(rec.get("human_review_status", "pending")).strip().lower()
    if status not in VALID_HUMAN_REVIEW_STATUSES:
        status = "pending"
    required: dict[str, bool] = {}
    non_boolean_required_checks: list[str] = []
    for field_name in REQUIRED_CHECK_FIELDS:
        parsed_value, is_strict_bool = _parse_strict_bool(rec, field_name)
        required[field_name] = parsed_value
        if not is_strict_bool:
            non_boolean_required_checks.append(field_name)
    failures = [name for name, ok in required.items() if not ok]
    outside_sandbox_activation_allowed = status == "accepted" and not failures
    return {
        "human_review_status": status,
        "required_checks": required,
        "non_boolean_required_checks": non_boolean_required_checks,
        "missing_or_failed_checks": failures,
        "outside_sandbox_activation_allowed": outside_sandbox_activation_allowed,
    }
