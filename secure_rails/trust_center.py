from pathlib import Path
import json, datetime
import subprocess

def validate(repo_root: Path) -> tuple[bool,list[str]]:
    req=[repo_root/'SECURITY.md',repo_root/'docs/secure-rails/trust-center.md',repo_root/'docs/secure-rails/vulnerability-disclosure-policy.md',repo_root/'docs/secure-rails/incident-response-runbook.md',repo_root/'docs/secure-rails/security-advisory-process.md',repo_root/'docs/secure-rails/customer-security-faq.md',repo_root/'docs/secure-rails/trust-center-control-matrix.md']
    errs=[f'missing: {p}' for p in req if not p.exists()]
    return (not errs, errs)

def build_data(repo_root: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    def run_check(cmd: list[str], tristate: bool = False) -> str:
        if tristate and len(cmd) >= 2 and cmd[1].endswith('.py'):
            script_path = repo_root / cmd[1]
            if not script_path.exists():
                return "not_run"
        try:
            ok = subprocess.run(cmd, cwd=repo_root, check=False).returncode == 0
            if ok:
                return "pass"
            return "fail"
        except Exception:
            return "not_run" if tristate else "fail"
    security_txt_status = "template_only"
    root_security_txt_path = repo_root / '.well-known/security.txt'
    docs_security_txt_path = repo_root / 'docs/.well-known/security.txt'
    security_txt_path = root_security_txt_path if root_security_txt_path.exists() else docs_security_txt_path
    if security_txt_path.exists():
        content = security_txt_path.read_text(encoding='utf-8').lower()
        security_txt_status = "pending_contact" if "example.invalid" in content else "generated"
    elif (repo_root / 'docs/secure-rails/templates/security.txt.template').exists():
        security_txt_status = "pending_contact"
    status={"schema_version":"securerails.trust_center_status.v1","generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"security_policy_present":(repo_root/'SECURITY.md').exists(),"vulnerability_disclosure_present":(repo_root/'docs/secure-rails/vulnerability-disclosure-policy.md').exists(),"security_txt_status":security_txt_status,"incident_response_runbook_present":(repo_root/'docs/secure-rails/incident-response-runbook.md').exists(),"security_advisory_process_present":(repo_root/'docs/secure-rails/security-advisory-process.md').exists(),"customer_security_faq_present":(repo_root/'docs/secure-rails/customer-security-faq.md').exists(),"control_matrix_present":(repo_root/'docs/secure-rails/trust-center-control-matrix.md').exists(),"claim_boundary_check":run_check(["python","scripts/secure_rails_claim_boundary_check.py","."], tristate=True),"safety_ledger_check":run_check(["python","scripts/secure_rails_safety_ledger_check.py","docs/secure-rails/templates/safety-ledger-example.json"], tristate=True),"no_automerge_check":run_check(["python","scripts/secure_rails_no_automerge_check.py","."], tristate=True),"utility_token_boundary_check":run_check(["python","-m","secure_rails","check-token-boundary","--repo-root","."], tristate=True),"certification_claims":"none","claim_boundary":"SecureRails Trust Center is readiness and evidence documentation, not a certification."}
    (out/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
    controls = [
        ("SEC-001","Claim-boundary enforcement","implemented"),
        ("SEC-002","No-auto-merge enforcement","implemented"),
        ("SEC-003","Safety ledger hard counters","implemented"),
        ("SEC-004","Redaction policy","partially implemented"),
        ("SEC-005","Work Vault validation","implemented"),
        ("SEC-006","MARK allocation record","implemented"),
        ("SEC-007","Sovereign assignment record","implemented"),
        ("SEC-008","ProofBundle generation","implemented"),
        ("SEC-009","Evidence Docket generation","implemented"),
        ("SEC-010","Vulnerability disclosure policy","implemented"),
        ("SEC-011","Incident response runbook","implemented"),
        ("SEC-012","Security advisory process","implemented"),
        ("SEC-013","Supply-chain provenance","implemented"),
        ("SEC-014","Customer pilot intake controls","implemented"),
        ("SEC-015","GitHub App least-privilege connector","implemented"),
        ("SEC-016","Template bootstrap health check","implemented"),
        ("SEC-017","$AGIALPHA utility-only boundary","implemented"),
        ("SEC-018","EU AI Act excluded-use posture","implemented"),
        ("SEC-019","Human review gate","implemented"),
        ("SEC-020","Evidence Mission Control publication guard","implemented"),
    ]
    control_matrix = {
        "schema_version": "securerails.trust_center_control_matrix.v1",
        "controls": [{"control_id": cid, "name": name, "status": status} for cid, name, status in controls],
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
    return status
