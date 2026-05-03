import json,os
from .claim_boundary import CLAIM_BOUNDARY
def score_mark(out_dir,vault):
    obj={"schema_version":"1.0.0","allocation_id":"mark-demo-001","vault_id":vault["vault_id"],"opportunity_id":"opportunity-workflow-permission-001","assigned_sovereign":vault["assigned_sovereign"],"risk_tier":"low","review_priority":"high","allocated_budget_proxy":100,"utility_asset":"$AGIALPHA","proof_required":True,"replay_required":True,"falsification_required":True,"human_review_required":True,"auto_merge_allowed":False,"promotion_without_evidence_allowed":False,"validators_required":2,"rejection_reason_if_any":"","claim_boundary":CLAIM_BOUNDARY}
    json.dump(obj,open(os.path.join(out_dir,'mark-allocation.json'),'w'),indent=2);return obj
