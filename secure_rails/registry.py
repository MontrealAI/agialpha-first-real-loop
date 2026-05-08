import json
from pathlib import Path

REQ = ['raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','social_engineering_content_count','unsafe_automerge_count','critical_safety_incidents']


def _load(path: Path):
    # Fail fast on malformed registry records so indexing does not hide corruption.
    return json.loads(path.read_text(encoding='utf-8'))


def build_indexes(registry):
    r = Path(registry)
    (r / 'indexes').mkdir(parents=True, exist_ok=True)
    w = list((r / 'work_vaults').glob('*.json')) if (r / 'work_vaults').exists() else []

    by_status = {}
    by_sovereign = {}
    by_safety = {'all_zero': [], 'missing': [], 'non_zero': []}
    by_risk_tier = {}
    by_human_review_status = {}

    for p in w:
        d = _load(p)
        vid = d.get('vault_id', p.stem)

        st = d.get('status', 'unavailable')
        by_status.setdefault(st, []).append(vid)

        sid = d.get('sovereign_id') or d.get('sovereign', {}).get('sovereign_id') or d.get('mark_allocation', {}).get('assigned_sovereign')
        if sid:
            by_sovereign.setdefault(sid, []).append(vid)

        risk_tier = d.get('mark_allocation', {}).get('risk_tier', 'unavailable')
        by_risk_tier.setdefault(risk_tier, []).append(vid)

        review_status = d.get('evidence', {}).get('human_review_status', 'unavailable')
        by_human_review_status.setdefault(review_status, []).append(vid)

        hs = d.get('hard_safety_counters', {})
        if any(k not in hs for k in REQ):
            by_safety['missing'].append(vid)
        elif any(hs.get(k, 0) != 0 for k in REQ):
            by_safety['non_zero'].append(vid)
        else:
            by_safety['all_zero'].append(vid)

    sdir = r / 'sovereigns'
    if sdir.exists():
        for sp in sdir.glob('*.json'):
            sd = _load(sp)
            sid = sd.get('sovereign_id', sp.stem)
            by_sovereign.setdefault(sid, by_sovereign.get(sid, []))

    for n, d in [
        ('by_status.json', by_status),
        ('by_sovereign.json', by_sovereign),
        ('by_safety_status.json', by_safety),
        ('by_risk_tier.json', by_risk_tier),
        ('by_human_review_status.json', by_human_review_status),
    ]:
        (r / 'indexes' / n).write_text(json.dumps(d, indent=2), encoding='utf-8')
