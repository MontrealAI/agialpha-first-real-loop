"""Safe PR planning helpers for RSI-GOVERNOR-001."""

from __future__ import annotations

from typing import Any, Dict


def prepare_safe_pr_plan(candidate_id: str, candidate_hash: str, delta: float, heldout_win_rate: float) -> Dict[str, Any]:
    return {
        "title": "RSI-GOVERNOR-001: propose executable governance-kernel promotion",
        "candidate_id": candidate_id,
        "candidate_hash": candidate_hash,
        "B6_advantage_delta_vs_B5": delta,
        "B6_heldout_win_rate": heldout_win_rate,
        "auto_merge": False,
        "human_review_required": True,
        "claim_boundary": "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.",
        "rollback_note": "Revert to incumbent governance kernel and keep candidate in rejected ledger if review fails.",
    }


__all__ = ["prepare_safe_pr_plan"]
