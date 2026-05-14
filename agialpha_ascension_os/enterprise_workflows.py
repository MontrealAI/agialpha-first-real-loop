
from .context import BOUNDARY
PACKS=["software_quality_pack","evidence_ops_pack","docs_ops_pack","compliance_readiness_docs_pack","procurement_fixture_analysis_pack","sales_enablement_fixture_pack","defensive_security_docs_pack","trust_center_readiness_pack","enterprise_pilot_readiness_pack"]
def build_job_packs(triage):
    jobs=[]
    for i,name in enumerate(PACKS,1):
        jobs.append({"job_id":f"jobpack-{i:03d}","workflow_type":name,"synthetic_inputs_used":True,"prohibited_actions_checked":True,"regulated_boundary_triage":triage["allowed_mode"],"validator_requirements":["claim_boundary","token_boundary","regulated_boundary","human_review_required"],"expected_artifacts":["proofbundle","evidence_docket","work_vault"],"proofbundle_plan":"deterministic local json","evidence_docket_plan":"deterministic local json",**BOUNDARY})
    return jobs
