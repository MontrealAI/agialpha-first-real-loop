from __future__ import annotations

from typing import Any


VALID_HUMAN_REVIEW_STATUSES = {"pending", "accepted", "needs_changes", "rejected"}


def evaluate_human_review_gate(record: dict[str, Any] | None) -> dict[str, Any]:
    """Evaluate local human-review requirements for sandbox-to-production activation."""
    rec = record or {}
    status = str(rec.get("human_review_status", "pending")).strip().lower()
    if status not in VALID_HUMAN_REVIEW_STATUSES:
        status = "pending"
    required = {
        "evidence_docket_present": bool(rec.get("evidence_docket_present", False)),
        "proofbundle_present": bool(rec.get("proofbundle_present", False)),
        "replay_pass": bool(rec.get("replay_pass", False)),
        "falsification_pass": bool(rec.get("falsification_pass", False)),
        "claim_boundary_pass": bool(rec.get("claim_boundary_pass", False)),
        "token_boundary_pass": bool(rec.get("token_boundary_pass", False)),
        "regulated_boundary_pass": bool(rec.get("regulated_boundary_pass", False)),
        "no_auto_merge": bool(rec.get("no_auto_merge", True)),
        "no_autonomous_persistence": bool(rec.get("no_autonomous_persistence", True)),
    }
    failures = [name for name, ok in required.items() if not ok]
    outside_sandbox_activation_allowed = status == "accepted" and not failures
    return {
        "human_review_status": status,
        "required_checks": required,
        "missing_or_failed_checks": failures,
        "outside_sandbox_activation_allowed": outside_sandbox_activation_allowed,
    }

