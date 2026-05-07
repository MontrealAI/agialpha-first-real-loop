from pathlib import Path

def collect_files(repo_root):
    out=[]
    for p in Path(repo_root).rglob('*'):
        if p.is_file() and '.git' not in p.parts:
            out.append(str(p.relative_to(repo_root)))
    return sorted(out)

def pr_diff_summary(repo_root):
    files=collect_files(repo_root)
    wf=[f for f in files if f.startswith('.github/workflows/')]
    docs=[f for f in files if f.startswith('docs/') or f.lower().startswith('readme')]
    return {'changed_files':files,'workflow_files':wf,'docs_files':docs,'claim_boundary':'SecureRails is AI-agent security governance and proof-bound defensive remediation.'}
