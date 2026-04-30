import json, re
from pathlib import Path
UNSAFE=["achieved agi","achieved asi","empirical sota","safe autonomy","real-world security certification","guaranteed economic return","civilization-scale capability"]

def validate_manifest(m):
    req=["schema_version","experiment_slug","claim_boundary","run_id","status"]
    for k in req:
        if not m.get(k): raise ValueError(f"missing {k}")
    cb=(m.get('claim_boundary') or '').lower()
    for t in UNSAFE:
        if t in cb and 'does not claim' not in cb:
            raise ValueError(f"unsafe claim: {t}")
    slug=(m.get('experiment_slug') or '').lower()
    if any(x in slug for x in ['cyber','gauntlet','security']):
        metrics=m.get('metrics') or {}
        for k in ["safety_incidents","policy_violations","raw_secret_leak_count","external_target_scan_count","exploit_execution_count","malware_generation_count","unsafe_automerge_count"]:
            if k not in metrics: raise ValueError(f"missing safety counter {k}")

def validate_site(site):
    if not (Path(site)/'index.html').exists(): raise ValueError('missing root index')
