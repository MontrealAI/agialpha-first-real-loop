from __future__ import annotations

from .context import BOUNDARIES


RECEIPT_NOTE = (
    "Synthetic local utility receipt only. No wallet, custody, payment, trading, KYC/AML, "
    "money transmission, securities functionality, token price, token value, token appreciation, "
    "or investment return."
)


def build_skill_work_vault_receipt(*, receipt_id: str, skill_id: str, source_job_id: str, source_agent_id: str, target_agent_ids: list[str], utility_budget_units: int = 100) -> dict:
    spent = 42 + 8 + 5 + 3 + 3 + 2 + len(target_agent_ids)
    if utility_budget_units < spent:
        raise ValueError(
            f"utility_budget_units ({utility_budget_units}) is lower than required spend ({spent}); "
            "refusing to emit underfunded synthetic receipt"
        )
    return {
        "schema_version": "agialpha.skill_network.work_vault_receipt.v1",
        "receipt_id": receipt_id,
        "skill_id": skill_id,
        "source_job_id": source_job_id,
        "source_agent_id": source_agent_id,
        "target_agent_ids": list(target_agent_ids),
        "utility_budget_units": utility_budget_units,
        "alpha_work_units_estimated": 42,
        "validator_fee_units": 8,
        "replay_fee_units": 5,
        "proofbundle_fee_units": 3,
        "evidence_docket_fee_units": 3,
        "skill_publication_fee_units": 2,
        "skill_import_fee_units": len(target_agent_ids),
        "unused_budget_refund_units": utility_budget_units - spent,
        "settlement_mode": "synthetic_local_json_receipt_only",
        "wallet_used": False,
        "custody_used": False,
        "payment_executed": False,
        "token_price_used": False,
        "investment_claim_made": False,
        "receipt_note": RECEIPT_NOTE,
        **BOUNDARIES,
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
        "no_auto_merge": True,
    }
