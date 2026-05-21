from __future__ import annotations

from typing import Any

from .metrics import SAFETY_COUNTERS, stronger_claim_supported


def compute_claim_support(metrics: dict[str, Any]) -> dict[str, Any]:
    supported = stronger_claim_supported(metrics)
    blockers: list[str] = []
    if not supported:
        if not (metrics.get("capabilities_frozen", 0) == metrics.get("capabilities_generated", -1) and metrics.get("capabilities_frozen", 0) > 0):
            blockers.append("capability_freeze_incomplete")
        if metrics.get("heldout_leakage_detected") is not False:
            blockers.append("heldout_leakage_detected_or_unavailable")
        if not (isinstance(metrics.get("treatment_score"), (int, float)) and isinstance(metrics.get("shadow_control_score"), (int, float)) and metrics["treatment_score"] > metrics["shadow_control_score"]):
            blockers.append("treatment_not_greater_than_control")
        if not (isinstance(metrics.get("improvement_delta"), (int, float)) and metrics["improvement_delta"] >= metrics.get("configured_minimum_threshold", 0.01)):
            blockers.append("improvement_delta_below_threshold")
        if metrics.get("metrics_computed_from_raw_results") is not True:
            blockers.append("metrics_not_computed_from_raw")
        if metrics.get("replay_pass") is not True:
            blockers.append("replay_not_passed")
        if metrics.get("falsification_pass") is not True:
            blockers.append("falsification_not_passed")
        if metrics.get("proofbundle_complete") is not True:
            blockers.append("proofbundle_incomplete")
        if metrics.get("evidence_docket_complete") is not True:
            blockers.append("evidence_docket_incomplete")
        if metrics.get("B4_rejected") is not True:
            blockers.append("b4_not_rejected")
        if metrics.get("B6_beats_B5_computed") is not True:
            blockers.append("b6_not_beating_b5")
        for counter in SAFETY_COUNTERS:
            if metrics.get(counter) != 0:
                blockers.append(f"safety_counter_nonzero:{counter}")
        if not blockers:
            blockers.append("unsupported_with_unclassified_blocker")
    return {
        "strong_claim_supported": supported,
        "claim_level": "engine_002_local_supported" if supported else "scaffold_or_partial_engine_evidence",
        "strong_claim_blockers": blockers,
    }
