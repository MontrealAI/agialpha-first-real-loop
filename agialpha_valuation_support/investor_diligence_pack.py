"""Investor diligence pack builder.

Boundary: non-promissory implementation-side evidence packaging only.
"""

from .boundaries import bfields, DISCLAIMER


def build_investor_diligence_pack() -> dict:
    return {
        "statement": DISCLAIMER,
        "pack_type": "implementation_side_evidence_only",
        **bfields(),
    }
