
from __future__ import annotations
import json, datetime
from pathlib import Path
REQUIRED_FILES = [
'README.md','docs/secure-rails/README.md','docs/secure-rails/product-boundary.md','docs/secure-rails/eu-ai-act-positioning.md',
'docs/secure-rails/foreseeable-misuse-and-excluded-uses.md','docs/secure-rails/work-vaults-mark-sovereigns.md','docs/secure-rails/templates/README.md',
'scripts/secure_rails_claim_boundary_check.py','scripts/secure_rails_safety_ledger_check.py','scripts/secure_rails_no_automerge_check.py','scripts/secure_rails_use_case_triage_check.py',
'.github/workflows/secure-rails-compliance-guard.yml']

def build_template_health(repo_root:Path, repository:str)->dict:
    missing=[f for f in REQUIRED_FILES if not (repo_root/f).exists()]
    warns=[]
    if not (repo_root/'docs/START_HERE.md').exists() and not (repo_root/'README.md').exists(): warns.append('missing START_HERE or equivalent')
    status='pass' if not missing else 'fail'
    return {'schema_version':'securerails.template_health.v1','generated_at':datetime.datetime.utcnow().isoformat()+'Z','repository':repository,
            'status':status,'checks':['required_files'],'missing_required_files':missing,'warnings':warns,'next_steps':['Run SecureRails Compliance Guard'],'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}

def write_template_health(repo_root:Path, repository:str, out:Path)->dict:
    h=build_template_health(repo_root, repository)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(h, indent=2), encoding='utf-8')
    return h
