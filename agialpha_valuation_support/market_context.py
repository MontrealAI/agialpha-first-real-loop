"""Deterministic market-context helpers for valuation-support dossiers.

Boundary: documentation-only scenario analysis; no valuation or investment claims.
"""

from .core import bfields


def build_market_context(comparables_count: int) -> dict:
    return {
        "comparables_count": comparables_count,
        **bfields(),
    }
