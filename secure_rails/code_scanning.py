from pathlib import Path
from datetime import datetime, timezone
import json

CLAIM='Code scanning readiness is advisory and not a security certification.'

def code_scanning_readiness(repo_root):
    root=Path(repo_root)
    langs=[]
    if list(root.rglob('*.py')): langs.append('python')
    workflow_present = False
    wf_dir = root / '.github' / 'workflows'
    if wf_dir.exists():
        for ext in ('*.yml', '*.yaml'):
            if any('codeql' in p.name.lower() for p in wf_dir.glob(ext)):
                workflow_present = True
                break
    status='ready' if langs else 'not_applicable'
    return {
      'schema_version':'securerails.code_scanning_readiness.v1','generated_at':datetime.now(timezone.utc).isoformat(),'repository':'',
      'codeql_supported_languages_detected':langs,'recommended_setup':'default_setup' if langs else 'not_applicable',
      'workflow_present':workflow_present,'status':status,'notes':['Enable GitHub default setup for CodeQL in repository settings.'] if langs else [],'claim_boundary':CLAIM
    }

def write_code_scanning_readiness(repo_root,out):
    d=code_scanning_readiness(repo_root); Path(out).write_text(json.dumps(d,indent=2)); return d
