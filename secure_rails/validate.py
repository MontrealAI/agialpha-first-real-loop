from __future__ import annotations
import json, subprocess
from pathlib import Path

def validate_registry(registry: Path) -> bool:
    ok=True
    for part in ('work_vaults','mark_allocations','sovereigns','settlements'):
        for p in sorted((registry/part).glob('*.json')):
            r=subprocess.run(['python','scripts/secure_rails_work_vault_check.py',str(p)], capture_output=True, text=True)
            if r.returncode!=0:
                print(r.stdout+r.stderr)
                ok=False
    return ok
