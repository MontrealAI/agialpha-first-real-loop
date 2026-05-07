from pathlib import Path


def review_workflows(repo_root, workflow_files=None):
    risks = []
    if workflow_files is None:
        candidates = list(Path(repo_root, '.github/workflows').glob('*.yml')) + list(Path(repo_root, '.github/workflows').glob('*.yaml'))
    else:
        candidates = [Path(repo_root, wf) for wf in workflow_files if wf.startswith('.github/workflows/') and (wf.endswith('.yml') or wf.endswith('.yaml'))]

    for p in candidates:
        if not p.exists() or not p.is_file():
            continue
        t = p.read_text(encoding='utf-8', errors='ignore')
        if 'pull_request_target' in t:
            risks.append({'file': str(p), 'risk': 'pull_request_target'})
        if 'permissions:' in t and ('write-all' in t or 'contents: write' in t):
            risks.append({'file': str(p), 'risk': 'broad_write_permissions'})
    return {'risks': risks, 'claim_boundary': 'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
