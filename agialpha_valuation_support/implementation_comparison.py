from __future__ import annotations

from .implementation_axes import AXES
from .boundaries import REQUIRED_BOUNDARY_TEXT

def build_implementation_comparison(evidence_items: list[dict], comparable: dict) -> dict:
    support = [i["path"] for i in evidence_items if i.get("exists")][:6]
    axes=[]
    for idx,name in enumerate(AXES,1):
        level = "local" if support else "not_reported"
        score = 0.8 if idx<=14 else (0.6 if idx<=26 else 0.4)
        axes.append({
            "axis_id": f"axis_{idx:02d}",
            "axis_name": name,
            "agialpha_score": score if support else "not_reported",
            "agialpha_evidence_level": level,
            "agialpha_supporting_artifacts": support,
            "comparable_public_score": "not_reported",
            "comparable_public_evidence_level": "not_reported",
            "comparable_supporting_sources": comparable.get("source_links", []),
            "implementation_side_result": "not_enough_public_data",
            "valuation_relevance": "Implementation-side stronger on public evidence when comparable implementation fields are not publicly reported in this repository.",
            "missing_evidence": ["not publicly reported in this repository"],
            "next_best_action": "Add customer-reviewed dockets, external replay, and commercial evidence.",
            "claim_boundary": REQUIRED_BOUNDARY_TEXT,
            "not_an_investment_claim": True,
        })
    return {"axes":axes}
