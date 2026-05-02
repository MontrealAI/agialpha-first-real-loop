"""FoundryPolicy RSI candidate evaluation helpers."""

from __future__ import annotations


def compare_policies(incumbent_score: float, candidate_score: float) -> dict:
    """Return promotion-safe policy comparison payload."""
    delta = round(candidate_score - incumbent_score, 6)
    return {
        "incumbent_score": incumbent_score,
        "candidate_score": candidate_score,
        "FoundryPolicy_advantage_delta": delta,
        "FoundryPolicy_vnext_beats_incumbent": delta > 0,
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
    }
