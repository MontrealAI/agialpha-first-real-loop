from .context import BOUNDARY
DISCLAIMER="This is a directional operational proxy, not a financial projection, investment claim, token-value claim, legal conclusion, or guaranteed economic result."
def compute(inputs):
    s=dict(inputs)
    value=s["verified_enterprise_alpha_score"]*s["reusable_capability_score"]*s["replay_integrity_score"]*s["governance_integrity_score"]*s["regulated_boundary_integrity_score"]/max(1,s["cost_risk_proxy"])
    return {"score":value,"inputs":s,"disclaimer":DISCLAIMER,**BOUNDARY}
