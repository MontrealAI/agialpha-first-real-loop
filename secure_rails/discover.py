from __future__ import annotations
import json, shutil
from pathlib import Path

MAP=[('work_vaults','work-vault-example.json','sr-vault-example-001.json'),('mark_allocations','mark-allocation-example.json','mark-alloc-example-001.json'),('sovereigns','sovereign-example.json','workflow-permission-sovereign.json'),('settlements','vault-settlement-example.json','settlement-example-001.json')]

def discover(repo_root: Path, registry: Path) -> None:
    tdir=repo_root/'docs'/'secure-rails'/'templates'
    for folder,src,dst in MAP:
        target=registry/folder/dst
        if target.exists():
            continue
        data=json.loads((tdir/src).read_text(encoding='utf-8'))
        data['source']='example_template'
        data['status']='example_not_production'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n", encoding='utf-8')
