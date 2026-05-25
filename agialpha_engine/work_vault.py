from __future__ import annotations

import hashlib
import json
from typing import Any

from .context import BOUNDARIES

RECEIPT_TEXT = (
    "Synthetic local utility receipt only. No wallet, custody, payment, trading, "
    "KYC/AML, money transmission, securities functionality, token price, token value, "
    "token appreciation, or investment return."
)


def _hash_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def make_skill_publication_receipt(*, run_id: str, skill_id: str, source_job_id: str, units: int = 1) -> dict[str, Any]:
    base = {
        "schema_version": "agialpha.skill_work_vault_receipt.v1",
        "receipt_id": f"receipt-{run_id}-{skill_id}",
        "run_id": run_id,
        "skill_id": skill_id,
        "source_job_id": source_job_id,
        "utility_units": int(units),
        "wallet_used": False,
        "custody_used": False,
        "payment_executed": False,
        "token_price_used": False,
        "investment_claim_made": False,
        "receipt_text": RECEIPT_TEXT,
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
        "no_auto_merge": True,
        **BOUNDARIES,
    }
    base["receipt_hash"] = _hash_payload(base)
    return base
