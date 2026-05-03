import json, os
from .claim_boundary import CLAIM_BOUNDARY
from .safety import HARD_COUNTERS

def create_work_vault(out_dir):
    os.makedirs(out_dir,exist_ok=True)
    counters={k:0 for k in HARD_COUNTERS}
    vault={"schema_version":"1.0.0","vault_id":"vault-demo-001","vault_type":"workflow_permission_review","status":"proposed","created_at":"2026-05-03T00:00:00Z","operator":"agialpha_securerails","scope":{"repo_owned":True},"utility":{"asset":"$AGIALPHA","budget_proxy":100},"mark_allocation":"mark-demo-001","assigned_sovereign":"sovereign-workflow-permission-001","validators":["policy-validator","replay-validator"],"hard_safety_counters":counters,"evidence":{"proofbundle_id":"proofbundle-demo-001","evidence_docket_id":"evidence-docket-demo-001"},"settlement":{"settlement_id":"settlement-demo-001","status":"pending"},"archive":{"capability_entry_id":"capability-demo-001"},"claim_boundary":CLAIM_BOUNDARY}
    json.dump(vault,open(os.path.join(out_dir,'work-vault.json'),'w'),indent=2)
    return vault
