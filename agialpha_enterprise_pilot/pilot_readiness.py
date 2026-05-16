from .boundaries import boundary_fields

DISCLAIMER = "Pilot Readiness Score is a directional operational readiness proxy. It is not a legal conclusion, compliance certification, security certification, ROI claim, investment claim, token-value claim, revenue forecast, or guarantee of business outcome."

def compute_pilot_readiness_score(*, evidence_docket_score=100, proofbundle_score=100, replay_readiness_score=100, regulated_boundary_integrity=100, secure_rails_integrity=100, customer_review_status_score=40, work_vault_integrity=100, missing_evidence_honesty=100, risk_cost_proxy=1, has_evidence_docket=True, has_proofbundle=True, has_replay=True, customer_review_status="pending"):
    if regulated_boundary_integrity == 0:
        raise ValueError("regulated boundary violation")
    raw = (evidence_docket_score * proofbundle_score * replay_readiness_score * regulated_boundary_integrity * secure_rails_integrity * customer_review_status_score * work_vault_integrity * missing_evidence_honesty) // (100**7 * max(1, risk_cost_proxy))
    cap = 100
    if not has_evidence_docket:
        cap = min(cap, 40)
    if not has_proofbundle:
        cap = min(cap, 50)
    if not has_replay:
        cap = min(cap, 60)
    if customer_review_status == "pending":
        cap = min(cap, 70)
    return {"pilot_readiness_score": min(raw, cap), "status": "directional_proxy", "wording": DISCLAIMER, **boundary_fields()}
