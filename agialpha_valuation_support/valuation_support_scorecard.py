from __future__ import annotations

def build_scorecard(eq: dict) -> dict:
    return {
        "valuation_support_readiness_tier": eq.get("readiness_tier", "T0"),
        "implementation_equivalence_score": eq.get("implementation_equivalence_score", "not_reported"),
        "tier_cap_reason": eq.get("tier_cap_reason", "not_reported"),
    }
