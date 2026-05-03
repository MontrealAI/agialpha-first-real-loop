import json,os
from .claim_boundary import CLAIM_BOUNDARY
def make_evidence_docket(out_dir,vault):
 o={"evidence_docket_id":"evidence-docket-demo-001","vault_id":vault["vault_id"],"human_review_status":"required","claim_boundary":CLAIM_BOUNDARY};json.dump(o,open(os.path.join(out_dir,"evidence-docket.json"),"w"),indent=2);return o
