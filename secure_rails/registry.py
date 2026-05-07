import json
from pathlib import Path

REQ = [
    'raw_secret_leak_count',
    'external_target_scan_count',
    'exploit_execution_count',
    'malware_generation_count',
    'social_engineering_content_count',
    'unsafe_automerge_count',
    'critical_safety_incidents',
]


def _load(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return {}


def build_indexes(registry):
    r = Path(registry)
    (r / 'indexes').mkdir(parents=True, exist_ok=True)
    w = list((r / 'work_vaults').glob('*.json')) if (r / 'work_vaults').exists() else []
    m = list((r / 'mark_allocations').glob('*.json')) if (r / 'mark_allocations').exists() else []

    by_status, by_sovereign = {}, {}
    by_safety = {'all_zero': [], 'missing': [], 'non_zero': []}

    for p in w:
        d = _load(p)
        vid = d.get('vault_id', p.stem)
        st = d.get('status', 'unavailable')
        by_status.setdefault(st, []).append(vid)

        sid = (
            d.get('sovereign_id')
            or d.get('sovereign', {}).get('sovereign_id')
            or d.get('mark_allocation', {}).get('assigned_sovereign')
        )
        if sid:
            by_sovereign.setdefault(sid, []).append(vid)

        hs = d.get('hard_safety_counters', {})
        if any(k not in hs for k in REQ):
            by_safety['missing'].append(vid)
        elif any(hs.get(k, 0) != 0 for k in REQ):
            by_safety['non_zero'].append(vid)
        else:
            by_safety['all_zero'].append(vid)

    for p in m:
        d = _load(p)
        sid = d.get('assigned_sovereign')
        vid = d.get('vault_id')
        if sid and vid:
            by_sovereign.setdefault(sid, []).append(vid)

    sdir = r / 'sovereigns'
    if sdir.exists():
        for sp in sdir.glob('*.json'):
            sid = _load(sp).get('sovereign_id', sp.stem)
            by_sovereign.setdefault(sid, [])

    # de-dup and sort for deterministic output
    for key, vals in by_sovereign.items():
        by_sovereign[key] = sorted(set(vals))

    for n, d in [
        ('by_status.json', by_status),
        ('by_sovereign.json', by_sovereign),
        ('by_safety_status.json', by_safety),
        ('by_risk_tier.json', {}),
        ('by_human_review_status.json', {}),
    ]:
        Path(r / 'indexes' / n).write_text(json.dumps(d, indent=2))
