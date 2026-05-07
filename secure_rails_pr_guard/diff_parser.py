from pathlib import Path
import subprocess


def collect_all_files(repo_root):
    out = []
    for p in Path(repo_root).rglob('*'):
        if p.is_file() and '.git' not in p.parts:
            out.append(str(p.relative_to(repo_root)))
    return sorted(out)


def _git_changed_files(repo_root, base_sha, head_sha):
    if not base_sha or not head_sha:
        return []
    cmd = ['git', '-C', str(repo_root), 'diff', '--name-only', '--merge-base', base_sha, head_sha]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def resolve_changed_files(repo_root, event):
    pr = (event or {}).get('pull_request') or {}
    base_sha = ((pr.get('base') or {}).get('sha'))
    head_sha = ((pr.get('head') or {}).get('sha'))
    changed = _git_changed_files(repo_root, base_sha, head_sha)
    return sorted(set(changed))


def pr_diff_summary(repo_root, event=None):
    files = resolve_changed_files(repo_root, event or {})
    wf = [f for f in files if f.startswith('.github/workflows/')]
    docs = [f for f in files if f.startswith('docs/') or f.lower().startswith('readme')]
    return {
        'changed_files': files,
        'workflow_files': wf,
        'docs_files': docs,
        'claim_boundary': 'SecureRails is AI-agent security governance and proof-bound defensive remediation.',
    }
