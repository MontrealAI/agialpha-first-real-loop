def build_validator_report(rec):
    return {'schema_version':'securerails.pr_validator_report.v1','recommendation':rec,'validators':['claim_boundary','no_automerge','secret_redaction','workflow_permissions'],'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
