def build_work_vault(ctx):
    return {'schema_version':'securerails.work_vault.v1','vault_type':'proof_bound_pr_review','work_vault_id':f"wv-pr-{ctx['pull_request']['number']}",'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
