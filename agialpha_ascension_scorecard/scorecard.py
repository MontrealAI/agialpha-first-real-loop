
from .claims import CLAIM_BOUNDARY_SHORT
AXES=[
"Public working artifact","One-command local run","Deterministic replay","Evidence Docket completeness","ProofBundle completeness","Recursive loop evidence","AI-improves-AI task evidence","Archive reuse / lineage metaproductivity","Open-ended discovery","Validator quality","Falsification audit","Safety and claim-boundary governance","Human-governed promotion","Work Vault / MARK / Sovereign linkage","$AGIALPHA utility-bound settlement","Business-operational usefulness","Value-to-capacity proxy","External replay readiness","Independent validation status","Public benchmark readiness"]

def build_scorecard():
    return {"axes":[{"axis_id":f"axis_{i+1:02d}","axis_name":name,"score":"not_reported","max_score":100,"evidence_level":"local" if i<8 else "not_reported","evidence_links":[],"supporting_artifacts":[],"claim_boundary":CLAIM_BOUNDARY_SHORT,"missing_evidence":["pending run artifacts"],"next_best_action":"Run Open RSI Eval lifecycle to populate."} for i,name in enumerate(AXES)]}
