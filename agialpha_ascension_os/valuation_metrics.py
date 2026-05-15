"""Deterministic valuation-support proxy math for Ascension OS.

These metrics are operational proxies only and are explicitly non-investment, non-token,
non-securities outputs.
"""

from __future__ import annotations

from typing import Mapping

VERIFIED_ENTERPRISE_ALPHA_STATEMENT = (
    "Verified Enterprise Alpha is a directional operational usefulness proxy, "
    "not ROI, financial projection, investment claim, token-value claim, legal conclusion, "
    "or guaranteed result."
)

VALUE_TO_CAPACITY_STATEMENT = (
    "Value-to-Capacity is a directional proxy, not a financial projection, energy claim, "
    "infrastructure ownership claim, utility-market claim, or superintelligence claim."
)

CAPACITY_REINVESTMENT_STATEMENT = (
    "Capacity Reinvestment is a planning proxy, not a financing plan, investment product, "
    "energy claim, utility-market claim, or guaranteed capacity expansion."
)


def _safe_number(data: Mapping[str, object], key: str) -> float:
    value = data.get(key, "not_reported")
    return float(value) if isinstance(value, (int, float)) else 0.0


def verified_enterprise_alpha(metrics: Mapping[str, object]) -> dict:
    cost_risk = max(1.0, _safe_number(metrics, "cost_risk_proxy"))
    score = (
        _safe_number(metrics, "verified_work_score")
        * _safe_number(metrics, "evidence_quality_score")
        * _safe_number(metrics, "replay_integrity_score")
        * _safe_number(metrics, "business_usefulness_score")
        * _safe_number(metrics, "reusable_capability_score")
        * _safe_number(metrics, "governance_integrity_score")
        * _safe_number(metrics, "regulated_boundary_integrity_score")
    ) / cost_risk
    return {"verified_enterprise_alpha_score": score, "statement": VERIFIED_ENTERPRISE_ALPHA_STATEMENT}


def value_to_capacity(metrics: Mapping[str, object]) -> dict:
    cost_risk = max(1.0, _safe_number(metrics, "cost_risk_proxy"))
    score = (
        _safe_number(metrics, "verified_work_score")
        * _safe_number(metrics, "reusable_capability_score")
        * _safe_number(metrics, "archive_reuse_score")
        * _safe_number(metrics, "business_usefulness_score")
        * _safe_number(metrics, "compute_or_infra_proxy_score")
        * _safe_number(metrics, "governance_integrity_score")
        * _safe_number(metrics, "regulated_boundary_integrity_score")
    ) / cost_risk
    return {"value_to_capacity_proxy": score, "statement": VALUE_TO_CAPACITY_STATEMENT}


def capacity_reinvestment(metrics: Mapping[str, object]) -> dict:
    cost_risk = max(1.0, _safe_number(metrics, "cost_risk_proxy"))
    score = (
        _safe_number(metrics, "verified_enterprise_alpha_score")
        * _safe_number(metrics, "reusable_capability_score")
        * _safe_number(metrics, "replay_integrity_score")
        * _safe_number(metrics, "governance_integrity_score")
        * _safe_number(metrics, "regulated_boundary_integrity_score")
    ) / cost_risk
    return {"capacity_reinvestment_proxy": score, "statement": CAPACITY_REINVESTMENT_STATEMENT}
