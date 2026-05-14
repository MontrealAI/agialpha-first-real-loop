"""Valuation-support readiness scorecard helpers."""

from .core import bfields


def build_scorecard() -> dict:
    return {
        "valuation_support_readiness_tier": "T0",
        "implementation_equivalence_score": "not_reported",
        **bfields(),
    }
