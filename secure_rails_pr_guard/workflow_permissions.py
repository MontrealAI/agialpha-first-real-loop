from pathlib import Path

def review_workflows(repo_root):
    risks=[]
    for p in Path(repo_root,'.github/workflows').glob('*.yml'):
        t=p.read_text(encoding='utf-8',errors='ignore')
        if 'pull_request_target' in t: risks.append({'file':str(p),'risk':'pull_request_target'})
        if 'permissions:' in t and ('write-all' in t or 'contents: write' in t): risks.append({'file':str(p),'risk':'broad_write_permissions'})
    return {'risks':risks,'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
