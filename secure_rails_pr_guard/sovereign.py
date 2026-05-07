def assign_sovereign(diff,workflow,secrets,claims,no_auto):
    primary='Claim Boundary Sovereign'
    secondary=[]
    if workflow['risks']: primary='Workflow Permission Sovereign'
    if secrets: secondary.append('Secret Hygiene Sovereign')
    if no_auto['findings']: secondary.append('Safe PR Remediation Sovereign')
    return {'schema_version':'securerails.sovereign_assignment.v1','primary':primary,'secondary':secondary,'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
