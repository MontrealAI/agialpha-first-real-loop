import json,os
from .claim_boundary import CLAIM_BOUNDARY
def assign_sovereign(out_dir):
 o={"schema_version":"1.0.0","sovereign_id":"sovereign-workflow-permission-001","sovereign_name":"Workflow Permission Sovereign","domain":"SecureRails","task_family":"workflow_permission_review","allowed_work":["repo-owned workflow permission review"],"forbidden_work":["offensive cyber","external scanning","exploit execution"],"validators":["policy-validator","replay-validator"],"proofbundle_policy":{"required":True},"evidence_docket_policy":{"required":True},"promotion_policy":{"autonomous_promotion_allowed":False,"human_review_required":True,"auto_merge_allowed":False},"archive_policy":{"enabled":True},"claim_boundary":CLAIM_BOUNDARY}
 json.dump(o,open(os.path.join(out_dir,'sovereign.json'),'w'),indent=2);return o
