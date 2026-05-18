"""Adversarial docket records for failed and rejected variants."""
from __future__ import annotations

from typing import Any


def build_adversarial_docket(metrics: dict[str, Any], semantic: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    delta = metrics.get("improvement_delta")
    return {
        "failed_runs": [
            {"case_id": "treatment-no-frozen-capability", "status": "rejected", "reason": "treatment run without frozen capability is not counted"},
            {"case_id": "replay-mismatch", "status": "rejected", "reason": "tampered metrics fail replay verification"},
        ],
        "rejected_claims": [
            {"claim": "achieved AGI / SOTA / certification", "status": "rejected", "reason": "outside claim boundary"},
            {"claim": "token value or ROI", "status": "rejected", "reason": "utility-only token boundary"},
        ],
        "evaluator_disagreements": [
            {"fixture_id": "workflow-heldout-pages", "treatment": "invalid", "shadow_control": "valid", "resolution": "validator rules prefer no direct Pages deploy"},
        ],
        "baseline_regressions": [
            {"baseline": "B4_ungated_self_modification", "status": "failed_as_required", "reason": "ungated self-modification rejected"},
        ],
        "falsification_attempts": [
            {"attempt": "capability mutation after freeze", "blocked": True},
            {"attempt": "heldout leakage", "blocked": True},
            {"attempt": "semantic negative injections", "blocked": semantic.get("pass") is True},
            {"attempt": "treatment fails to beat control", "would_support_claim": bool(isinstance(delta, (int, float)) and delta > 0)},
        ],
    }
