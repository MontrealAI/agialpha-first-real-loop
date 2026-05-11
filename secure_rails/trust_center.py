from pathlib import Path
import json, datetime
import subprocess
import re

def validate(repo_root: Path) -> tuple[bool,list[str]]:
    req=[repo_root/'SECURITY.md',repo_root/'docs/secure-rails/trust-center.md',repo_root/'docs/secure-rails/vulnerability-disclosure-policy.md',repo_root/'docs/secure-rails/incident-response-runbook.md',repo_root/'docs/secure-rails/security-advisory-process.md',repo_root/'docs/secure-rails/customer-security-faq.md',repo_root/'docs/secure-rails/trust-center-control-matrix.md']
    errs=[f'missing: {p}' for p in req if not p.exists()]
    return (not errs, errs)

def build_data(repo_root: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    def run_check(cmd: list[str], tristate: bool = False) -> str:
        try:
            ok = subprocess.run(cmd, cwd=repo_root, check=False).returncode == 0
            return "pass" if ok else "fail"
        except Exception:
            return "not_run" if tristate else "fail"
    status={"schema_version":"securerails.trust_center_status.v1","generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"security_policy_present":(repo_root/'SECURITY.md').exists(),"vulnerability_disclosure_present":(repo_root/'docs/secure-rails/vulnerability-disclosure-policy.md').exists(),"security_txt_status":"pending_contact","incident_response_runbook_present":(repo_root/'docs/secure-rails/incident-response-runbook.md').exists(),"security_advisory_process_present":(repo_root/'docs/secure-rails/security-advisory-process.md').exists(),"customer_security_faq_present":(repo_root/'docs/secure-rails/customer-security-faq.md').exists(),"control_matrix_present":(repo_root/'docs/secure-rails/trust-center-control-matrix.md').exists(),"claim_boundary_check":run_check(["python","scripts/secure_rails_claim_boundary_check.py","."], tristate=True),"safety_ledger_check":run_check(["python","scripts/secure_rails_safety_ledger_check.py","docs/secure-rails/templates/safety-ledger-example.json"], tristate=True),"no_automerge_check":run_check(["python","scripts/secure_rails_no_automerge_check.py","."], tristate=True),"utility_token_boundary_check":run_check(["python","-m","secure_rails","check-token-boundary","--repo-root","."], tristate=True),"certification_claims":"none","claim_boundary":"SecureRails Trust Center is readiness and evidence documentation, not a certification."}
    (out/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
    controls = []
    matrix_path = repo_root / 'docs/secure-rails/trust-center-control-matrix.md'
    if matrix_path.exists():
        for line in matrix_path.read_text(encoding='utf-8').splitlines():
            if not line.strip().startswith('| SEC-'):
                continue
            parts = [p.strip() for p in line.strip().strip('|').split('|')]
            if len(parts) >= 3 and re.match(r'^SEC-\d{3}$', parts[0]):
                controls.append({"control_id": parts[0], "name": parts[1], "status": parts[2]})
    control_matrix = {
        "schema_version": "securerails.trust_center_control_matrix.v1",
        "controls": controls,
    }
    (out/'control_matrix.json').write_text(json.dumps(control_matrix, indent=2), encoding='utf-8')
    disclosure_status = {
        "schema_version": "securerails.trust_center_disclosure.v1",
        "private_reporting": "enabled_or_pending_admin_enablement",
        "policy_present": (repo_root/'docs/secure-rails/vulnerability-disclosure-policy.md').exists(),
    }
    (out/'disclosure_status.json').write_text(json.dumps(disclosure_status, indent=2), encoding='utf-8')
    incident_example = repo_root / 'docs/secure-rails/templates/security-incident-record-example.json'
    incidents = []
    if incident_example.exists():
        try:
            incidents = [json.loads(incident_example.read_text(encoding='utf-8'))]
        except Exception:
            incidents = []
    latest_incidents = {"schema_version": "securerails.trust_center_incidents.v1", "incidents": incidents}
    (out/'latest_incidents.json').write_text(json.dumps(latest_incidents, indent=2), encoding='utf-8')
