"""Moat-assessment artifact generator for valuation support."""

from .core import bfields


def build_moat_assessment() -> dict:
    return {
        "assessment": "documentation_only",
        **bfields(),
    }
