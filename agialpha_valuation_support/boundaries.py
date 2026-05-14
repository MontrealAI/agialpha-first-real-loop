"""Shared valuation-support boundary constants and helpers."""

DISCLAIMER = (
    "AGI ALPHA does not assert a valuation in this document. "
    "This dossier organizes implementation-side evidence that may support a "
    "valuation-comparable discussion. It is not investment advice, financial advice, "
    "a securities offering, a token-value claim, a guarantee of return, "
    "or a fair-market-value opinion."
)


def bfields() -> dict:
    return {
        "claim_boundary": "valuation-support evidence only",
        "token_boundary": "utility-only $AGIALPHA; no token value claim",
        "regulated_boundary": "documentation_only",
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
        "no_auto_merge": True,
    }
