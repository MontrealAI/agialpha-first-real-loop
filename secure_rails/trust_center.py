from pathlib import Path
import json, datetime

def validate(repo_root: Path) -> tuple[bool,list[str]]:
    req=[repo_root/'SECURITY.md',repo_root/'docs/secure-rails/trust-center.md',repo_root/'docs/secure-rails/vulnerability-disclosure-policy.md',repo_root/'docs/secure-rails/incident-response-runbook.md',repo_root/'docs/secure-rails/security-advisory-process.md',repo_root/'docs/secure-rails/customer-security-faq.md',repo_root/'docs/secure-rails/trust-center-control-matrix.md']
    errs=[f'missing: {p}' for p in req if not p.exists()]
    return (not errs, errs)

def build_data(repo_root: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    status={"schema_version":"securerails.trust_center_status.v1","generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"security_policy_present":(repo_root/'SECURITY.md').exists(),"vulnerability_disclosure_present":(repo_root/'docs/secure-rails/vulnerability-disclosure-policy.md').exists(),"security_txt_status":"pending_contact","incident_response_runbook_present":(repo_root/'docs/secure-rails/incident-response-runbook.md').exists(),"security_advisory_process_present":(repo_root/'docs/secure-rails/security-advisory-process.md').exists(),"customer_security_faq_present":(repo_root/'docs/secure-rails/customer-security-faq.md').exists(),"control_matrix_present":(repo_root/'docs/secure-rails/trust-center-control-matrix.md').exists(),"claim_boundary_check":"pass","safety_ledger_check":"not_run","no_automerge_check":"not_run","utility_token_boundary_check":"not_run","certification_claims":"none","claim_boundary":"SecureRails Trust Center is readiness and evidence documentation, not a certification."}
    (out/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
