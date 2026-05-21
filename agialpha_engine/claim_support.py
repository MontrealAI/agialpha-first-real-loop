from __future__ import annotations

from typing import Any

from .metrics import stronger_claim_supported


def compute_claim_support(metrics: dict[str, Any]) -> dict[str, Any]:
    supported = stronger_claim_supported(metrics)
    blockers: list[str] = []
    if not supported:
        if metrics.get("metrics_computed_from_raw_results") is not True:
            blockers.append("metrics_not_computed_from_raw")
        if metrics.get("replay_pass") is not True:
            blockers.append("replay_not_passed")
        if metrics.get("falsification_pass") is not True:
            blockers.append("falsification_not_passed")
        if metrics.get("B6_beats_B5_computed") is not True:
            blockers.append("b6_not_beating_b5")
    return {
        "strong_claim_supported": supported,
        "claim_level": "engine_002_local_supported" if supported else "scaffold_or_partial_engine_evidence",
        "strong_claim_blockers": blockers,
    }
