from __future__ import annotations
import json
from pathlib import Path


def _load_dir(d: Path):
    if not d.exists():
        return []
    return [json.loads(p.read_text(encoding='utf-8')) for p in sorted(d.glob('*.json'))]


def build_indexes(registry: Path) -> None:
    registry.mkdir(parents=True, exist_ok=True)
    (registry / 'indexes').mkdir(parents=True, exist_ok=True)
    w=_load_dir(registry/'work_vaults')
    m=_load_dir(registry/'mark_allocations')
    s=_load_dir(registry/'sovereigns')
    st=_load_dir(registry/'settlements')
    data={'generated_at':'1970-01-01T00:00:00Z','work_vaults':w,'mark_allocations':m,'sovereigns':s,'settlements':st}
    (registry/'registry.json').write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    (registry/'latest.json').write_text(json.dumps({'counts':{'work_vaults':len(w),'mark_allocations':len(m),'sovereigns':len(s),'settlements':len(st)}},indent=2,sort_keys=True)+"\n")
    for name,val in [('work_vaults.json',w),('mark_allocations.json',m),('sovereigns.json',s),('settlements.json',st)]:
        (registry/name).write_text(json.dumps(val,indent=2,sort_keys=True)+"\n")

    by_status = {}
    by_risk = {}
    by_human = {}
    by_safety = {"all_zero": [], "nonzero": [], "missing": []}
    counters=['raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','social_engineering_content_count','unsafe_automerge_count','critical_safety_incidents']
    for vault in w:
        vid=vault.get('vault_id','unavailable')
        by_status.setdefault(vault.get('status', 'unavailable'), []).append(vid)
        by_risk.setdefault(vault.get('mark_allocation',{}).get('risk_tier','unavailable'), []).append(vid)
        by_human.setdefault(vault.get('evidence',{}).get('human_review_status','not_reported'), []).append(vid)
        hs=vault.get('hard_safety_counters')
        if not isinstance(hs, dict):
            by_safety['missing'].append(vid)
        elif all(hs.get(k,0)==0 for k in counters):
            by_safety['all_zero'].append(vid)
        else:
            by_safety['nonzero'].append(vid)

    by_sovereign = {
        sovereign.get('sovereign_id', 'unknown'): [
            vault.get('vault_id')
            for vault in w
            if vault.get('mark_allocation', {}).get('assigned_sovereign') == sovereign.get('sovereign_id')
        ]
        for sovereign in s
    }
    (registry/'indexes'/'by_status.json').write_text(json.dumps(by_status,indent=2,sort_keys=True)+"\n")
    (registry/'indexes'/'by_sovereign.json').write_text(json.dumps(by_sovereign,indent=2,sort_keys=True)+"\n")
    (registry/'indexes'/'by_risk_tier.json').write_text(json.dumps(by_risk,indent=2,sort_keys=True)+"\n")
    (registry/'indexes'/'by_human_review_status.json').write_text(json.dumps(by_human,indent=2,sort_keys=True)+"\n")
    (registry/'indexes'/'by_safety_status.json').write_text(json.dumps(by_safety,indent=2,sort_keys=True)+"\n")
