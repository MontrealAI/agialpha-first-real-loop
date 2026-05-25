from __future__ import annotations

from .context import BOUNDARIES


def synthesize_local_settlement(receipt: dict) -> dict:
    return {
        "settlement_id": f"settlement-{receipt.get('receipt_id', 'unknown')}",
        "mode": "synthetic_local_json_receipt_only",
        "wallet_used": False,
        "custody_used": False,
        "payment_executed": False,
        "token_price_used": False,
        "investment_claim_made": False,
        "status": "recorded",
        **BOUNDARIES,
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
        "no_auto_merge": True,
    }
