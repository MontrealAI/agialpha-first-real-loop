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


def make_skill_publication_receipt(
    *,
    run_id: str,
    skill_id: str,
    source_job_id: str,
    source_agent_id: str,
    target_agent_ids: list[str],
    utility_budget_units: float = 100.0,
    alpha_work_units_estimated: float = 42.0,
    validator_fee_units: float = 8.0,
    replay_fee_units: float = 5.0,
    proofbundle_fee_units: float = 3.0,
    evidence_docket_fee_units: float = 3.0,
    skill_publication_fee_units: float = 2.0,
    skill_import_fee_units: float | None = None,
) -> dict[str, Any]:
    if not run_id or not skill_id or not source_job_id or not source_agent_id:
        raise ValueError("run_id, skill_id, source_job_id, and source_agent_id are required")
    if not target_agent_ids or any(not agent_id for agent_id in target_agent_ids):
        raise ValueError("target_agent_ids must contain at least one non-empty agent id")

    import_fee_units = float(skill_import_fee_units if skill_import_fee_units is not None else len(target_agent_ids))
    used_units = (
        float(alpha_work_units_estimated)
        + float(validator_fee_units)
        + float(replay_fee_units)
        + float(proofbundle_fee_units)
        + float(evidence_docket_fee_units)
        + float(skill_publication_fee_units)
        + import_fee_units
    )
    refund_units = max(0.0, float(utility_budget_units) - used_units)

    base = {
        "schema_version": "agialpha.skill_work_vault_receipt.v1",
        "receipt_id": f"receipt-{run_id}-{skill_id}",
        "run_id": run_id,
        "skill_id": skill_id,
        "source_job_id": source_job_id,
        "source_agent_id": source_agent_id,
        "target_agent_ids": target_agent_ids,
        "utility_budget_units": float(utility_budget_units),
        "alpha_work_units_estimated": float(alpha_work_units_estimated),
        "validator_fee_units": float(validator_fee_units),
        "replay_fee_units": float(replay_fee_units),
        "proofbundle_fee_units": float(proofbundle_fee_units),
        "evidence_docket_fee_units": float(evidence_docket_fee_units),
        "skill_publication_fee_units": float(skill_publication_fee_units),
        "skill_import_fee_units": import_fee_units,
        "unused_budget_refund_units": refund_units,
        "settlement_mode": "synthetic_local_json_receipt_only",
        "wallet_used": False,
        "custody_used": False,
        "payment_executed": False,
        "token_price_used": False,
        "investment_claim_made": False,
        "receipt_note": RECEIPT_TEXT,
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
        "no_auto_merge": True,
        **BOUNDARIES,
    }
    base["receipt_hash"] = _hash_payload(base)
    return base
