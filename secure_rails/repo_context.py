
from __future__ import annotations
import json
import subprocess
from pathlib import Path

def detect_repo_context(repo_root: Path) -> dict:
    owner = "unknown"
    repository = repo_root.resolve().name
    full_repository = f"{owner}/{repository}"
    try:
        remote = subprocess.check_output(['git','-C',str(repo_root),'config','--get','remote.origin.url'], text=True).strip()
        if remote:
            if remote.endswith('.git'):
                remote = remote[:-4]
            if 'github.com' in remote:
                tail = remote.split('github.com')[-1].lstrip(':/')
                if '/' in tail:
                    owner, repository = tail.split('/',1)
                    full_repository = f"{owner}/{repository}"
    except Exception:
        pass
    pages = f"https://{owner.lower()}.github.io/{repository}/" if owner != 'unknown' else ''
    return {
        'owner': owner,
        'repository': repository,
        'full_repository': full_repository,
        'public_pages_url': pages,
        'evidence_mission_control_url': pages,
    }

def write_detected_context(repo_root: Path, out: Path) -> dict:
    ctx = detect_repo_context(repo_root)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ctx, indent=2), encoding='utf-8')
    return ctx
