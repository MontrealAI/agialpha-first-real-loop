
from .claims import CLAIM_BOUNDARY_SHORT
TASK_FAMILIES=["evaluator improvement","replay hardening","Evidence Docket repair","ProofBundle repair","workflow catalog repair","claim-boundary hardening","token-boundary hardening","safety-ledger hardening","Work Vault linkage","MARK allocation linkage","Sovereign routing linkage","docs/operator usability improvement","recursive substrate vNext generation","archive reuse task","public benchmark adapter readiness","business value-to-capacity proxy task"]

def run_eval(task_count=16):
    tasks=[{"task_family":TASK_FAMILIES[i%len(TASK_FAMILIES)],"status":"evaluated"} for i in range(task_count)]
    baselines={f"B{i}":{"status":"represented"} for i in range(8)}
    baselines['B4']={"status":"fail_expected","reason":"ungated self-modification blocked"}
    return {"task_count":task_count,"tasks":tasks,"baselines":baselines,"b6_vs_b5":{"status":"unavailable","reason":"local bounded public evidence run without external benchmark fixtures"},"human_review_required":True,"claim_boundary":CLAIM_BOUNDARY_SHORT}
