"""Risk and boundary summary artifact helper."""

from .boundaries import bfields


def build_risk_boundary() -> dict:
    return {
        "risk_boundary": "regulated and claim boundaries enforced",
        **bfields(),
    }
