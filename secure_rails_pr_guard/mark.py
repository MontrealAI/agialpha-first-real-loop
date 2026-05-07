def allocate_mark(diff,workflow,claims,no_auto):
    tier='low'
    reasons=[]
    if diff['workflow_files'] or workflow['risks']:
        tier='medium'; reasons.append('workflow_or_docs_change')
    if workflow['risks'] or claims['violations']:
        tier='high'; reasons.append('permission_or_claim_risk')
    if no_auto['findings']:
        tier='critical'; reasons.append('auto_merge_enablement')
    return {'schema_version':'securerails.mark_allocation.v1','risk_tier':tier,'reasons':reasons,'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
