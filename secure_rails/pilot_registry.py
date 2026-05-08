import json
from datetime import datetime, timezone
from pathlib import Path


def ensure_registry(root: Path):
    (root/"customers").mkdir(parents=True, exist_ok=True)
    (root/"repos").mkdir(exist_ok=True)
    (root/"pilot_runs").mkdir(exist_ok=True)
    (root/"artifacts").mkdir(exist_ok=True)
    (root/"indexes").mkdir(exist_ok=True)
    for f,d in [("registry.json", {"records": []}), ("latest.json", {})]:
        p=root/f
        if not p.exists(): p.write_text(json.dumps(d, indent=2), encoding='utf-8')

def add_record(root: Path, rec: dict):
    ensure_registry(root)
    rp=root/"registry.json"
    db=json.loads(rp.read_text(encoding='utf-8'))
    rec=dict(rec)
    rec["ingested_at"]=datetime.now(timezone.utc).isoformat()
    db.setdefault("records", []).append(rec)
    rp.write_text(json.dumps(db, indent=2), encoding='utf-8')
    (root/"latest.json").write_text(json.dumps(rec, indent=2), encoding='utf-8')

def validate_registry(root: Path):
    p=root/"registry.json"
    if not p.exists(): return False
    db=json.loads(p.read_text(encoding='utf-8'))
    return isinstance(db.get("records"), list)
