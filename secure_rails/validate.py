from __future__ import annotations
import subprocess
import sys
from pathlib import Path

def validate_registry(registry: Path) -> bool:
    repo_root = Path(__file__).resolve().parent.parent
    validator = repo_root / 'scripts' / 'secure_rails_work_vault_check.py'
    ok=True
    for part in ('work_vaults','mark_allocations','sovereigns','settlements'):
        for p in sorted((registry/part).glob('*.json')):
            r=subprocess.run([sys.executable, str(validator), str(p)], capture_output=True, text=True)
            if r.returncode!=0:
                print(r.stdout+r.stderr)
                ok=False
    return ok
