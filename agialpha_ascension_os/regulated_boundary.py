
from .context import BOUNDARY
FLAGS=["financial_advice","investment_advice","payment_or_custody","wallet_or_trading","kyc_aml","legal_advice","medical_advice","hr_or_worker_evaluation","credit_or_lending","insurance","critical_infrastructure_control","energy_market_or_utility_market","biometric_identification","emotion_recognition","law_enforcement","migration_or_border","education_access_or_scoring","justice_or_democratic_process","offensive_cyber"]
def triage(intake_id,workflow_name,requested_flags=None):
    requested_flags=requested_flags or {}
    flags={k:bool(requested_flags.get(k,False)) for k in FLAGS}
    blocked=any(flags.values())
    mode='blocked_human_review_required' if blocked else 'safe_enterprise_workflow'
    reason='regulated_boundary_blocked' if blocked else 'synthetic non-regulated workflow'
    return {"schema_version":"agialpha.regulated_boundary_triage.v1","intake_id":intake_id,"workflow_name":workflow_name,"synthetic_fixture_only":True,"real_customer_data_used":False,"pii_used":False,"regulated_domain_flags":flags,"allowed_mode":mode,"reason":reason,**BOUNDARY}
