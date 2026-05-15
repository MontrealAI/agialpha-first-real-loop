from __future__ import annotations

REQUIRED_BOUNDARY_TEXT = "AGI ALPHA does not assert a valuation. This dossier organizes implementation-side evidence that may support a valuation-comparable discussion. It is not investment advice, financial advice, a securities offering, a token-value claim, a guarantee of return, or a fair-market-value opinion."
COMPARISON_LIMIT_TEXT = "Any comparison to private self-improving-AI labs is limited to public implementation-side evidence available in this repository and manually entered public comparables. Missing external data is shown as not_reported."
STRATEGIC_DIRECTION_TEXT = "AGI ALPHA’s long-horizon superintelligence / Kardashev / value-to-energy framing is a strategic direction, not a present achievement claim. Near-term valuation support must be based only on verified work, replay, Evidence Dockets, ProofBundles, Work Vaults, enterprise workflow evidence, customer-reviewed dockets if available, commercial-readiness evidence, and governance integrity."

def boundary_fields() -> dict:
    return {
        "claim_boundary": REQUIRED_BOUNDARY_TEXT,
        "comparison_limit_text": COMPARISON_LIMIT_TEXT,
        "strategic_direction_text": STRATEGIC_DIRECTION_TEXT,
        "not_an_investment_claim": True,
        "human_review_required": True,
        "no_autonomous_persistence": True,
        "no_auto_merge": True,
    }

bfields = boundary_fields
