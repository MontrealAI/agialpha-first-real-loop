from __future__ import annotations
import json
import hashlib
from pathlib import Path

MAP=[('work_vaults','work-vault-example.json','sr-vault-example-001.json'),('mark_allocations','mark-allocation-example.json','mark-alloc-example-001.json'),('sovereigns','sovereign-example.json','workflow-permission-sovereign.json'),('settlements','vault-settlement-example.json','settlement-example-001.json')]


def _stamp(data: dict, source: str, source_file: str) -> dict:
    raw=json.dumps(data, sort_keys=True, separators=(",",":"))
    out=dict(data)
    out['source'] = source
    out['status'] = 'example_not_production'
    out.setdefault('generated_at', '1970-01-01T00:00:00Z')
    out.setdefault('source_file', source_file)
    out.setdefault('source_hash', hashlib.sha256(raw.encode('utf-8')).hexdigest())
    return out


def discover(repo_root: Path, registry: Path) -> None:
    tdir=repo_root/'docs'/'secure-rails'/'templates'
    for folder,src,dst in MAP:
        target=registry/folder/dst
        if target.exists():
            continue
        source_path=tdir/src
        data=json.loads(source_path.read_text(encoding='utf-8'))
        data=_stamp(data, 'example_template', str(source_path))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n", encoding='utf-8')
