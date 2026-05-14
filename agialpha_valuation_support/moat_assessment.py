"""Moat-assessment artifact generator for valuation support."""

from .boundaries import bfields


def build_moat_assessment() -> dict:
    return {
        "assessment": "documentation_only",
        **bfields(),
    }
