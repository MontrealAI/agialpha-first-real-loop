"""Promotion gates for Foundry outputs and policy updates."""

from __future__ import annotations


def promotion_gate(*, replay_passed: bool, falsification_passed: bool, evidence_docket_present: bool, human_review: bool) -> dict:
    """Evaluate non-autonomous promotion constraints."""
    approved = bool(replay_passed and falsification_passed and evidence_docket_present and human_review)
    return {
        "eligible_for_pr": approved,
        "persisted": False,
        "autonomous_persistence_allowed": False,
        "reason": "human_review_required" if not human_review else "ready_for_manual_pr" if approved else "failed_gates",
    }
