from __future__ import annotations
import json
from pathlib import Path

def _load_dir(d: Path):
    return [json.loads(p.read_text(encoding='utf-8')) for p in sorted(d.glob('*.json'))]

def build_indexes(registry: Path) -> None:
    registry.mkdir(parents=True, exist_ok=True)
    (registry / 'indexes').mkdir(parents=True, exist_ok=True)
    w=_load_dir(registry/'work_vaults'); m=_load_dir(registry/'mark_allocations'); s=_load_dir(registry/'sovereigns'); st=_load_dir(registry/'settlements')
    data={'generated_at':'1970-01-01T00:00:00Z','work_vaults':w,'mark_allocations':m,'sovereigns':s,'settlements':st}
    (registry/'registry.json').write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    (registry/'latest.json').write_text(json.dumps({'counts':{'work_vaults':len(w),'mark_allocations':len(m),'sovereigns':len(s),'settlements':len(st)}},indent=2,sort_keys=True)+"\n")
    for name,val in [('work_vaults.json',w),('mark_allocations.json',m),('sovereigns.json',s),('settlements.json',st)]:
        (registry/name).write_text(json.dumps(val,indent=2,sort_keys=True)+"\n")
    by_status: dict[str, list[str]] = {}
    for vault in w:
        status = vault.get('status', 'unavailable')
        vault_id = vault.get('vault_id')
        if not vault_id:
            continue
        by_status.setdefault(status, []).append(vault_id)
    for status in by_status:
        by_status[status] = sorted(by_status[status])
    (registry/'indexes'/'by_status.json').write_text(json.dumps(by_status,indent=2,sort_keys=True)+"\n")
    by_sovereign = {
        sovereign.get('sovereign_id', 'unknown'): [
            vault.get('vault_id')
            for vault in w
            if vault.get('mark_allocation', {}).get('assigned_sovereign') == sovereign.get('sovereign_id')
        ]
        for sovereign in s
    }
    (registry/'indexes'/'by_sovereign.json').write_text(json.dumps(by_sovereign,indent=2,sort_keys=True)+"\n")
    for n in ('by_risk_tier.json','by_human_review_status.json','by_safety_status.json'):
        (registry/'indexes'/n).write_text('{}\n')
