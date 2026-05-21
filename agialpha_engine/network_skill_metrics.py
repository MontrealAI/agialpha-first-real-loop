from __future__ import annotations

from .context import BOUNDARIES


def base_record(extra=None):
    rec={**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True})
    return rec

__doc__ = "Network skill metrics computation from raw logs."

def compute_d_metric(rows):
    if not rows: return None
    return sum(r["success_score"]*r["validator_pass"]*r["replay_pass"]*r["proofbundle"]*r["docket"]/max(1,r["cost_risk_proxy"]) for r in rows)/len(rows)
