import json,re
from pathlib import Path
from .safety import SECURITY_COUNTERS
UNSAFE=["achieved agi","achieved asi","empirical sota","safe autonomy","real-world security certification","guaranteed economic return","guaranteed investment","civilization-scale capability","official public benchmark victory"]


def validate_manifest(m):
    for k in ['schema_version','experiment_slug','workflow_name','claim_boundary']:
        if not m.get(k): raise ValueError(f'missing {k}')
    if m.get('source')!='historical_backfill' and not m.get('run_id'): raise ValueError('missing run_id')
    if m.get('source')!='historical_backfill' and not m.get('run_url'): raise ValueError('missing run_url')
    txt=(m.get('claim_boundary','')+' '+m.get('experiment_name','')).lower()
    for p in UNSAFE:
        if p in txt and not any(n in txt for n in ['does not claim','not empirical sota','not real-world security certification','not claim']):
            raise ValueError('unsafe claim detected')
    metrics=m.get('metrics',{})
    if any(s in m.get('experiment_slug','') for s in ['cyber','gauntlet','omega','security']):
        for k in SECURITY_COUNTERS:
            if k not in metrics: raise ValueError(f'missing safety counter {k}')

def validate_registry(base='evidence_registry'):
    runs=json.loads((Path(base)/'runs.json').read_text()) if (Path(base)/'runs.json').exists() else []
    for r in runs: validate_manifest(r)

def validate_site(site):
    p=Path(site)
    for req in ['index.html','data/runs.json','experiments/index.html','runs/index.html']:
        if not (p/req).exists(): raise ValueError(f'missing site file {req}')
