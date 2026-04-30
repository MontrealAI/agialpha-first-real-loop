import re, json
from pathlib import Path
from .safety import SECURITY_COUNTERS
UNSAFE=[r'achieved agi',r'achieved asi',r'empirical sota',r'safe autonomy',r'real-world security certification',r'guaranteed economic return',r'guaranteed investment',r'civilization-scale capability',r'official public benchmark victory']
NEG=[r'does not claim',r'not empirical sota',r'not real-world security certification',r'does not claim safe autonomy']

def default_manifest(slug):
    metrics={k:'not_reported' for k in SECURITY_COUNTERS}
    return {"schema_version":"agialpha.evidence_run.v1","experiment_slug":slug,"experiment_name":slug.upper(),"experiment_family":slug.split('-')[0],"workflow_name":"historical_backfill","workflow_file":"unknown","run_id":f"historical-{slug}","run_attempt":"1","run_url":"","commit_sha":"historical","branch":"main","actor":"backfill","event":"backfill","generated_at":"","status":"discovered","conclusion":"unknown","claim_level":"historical-local","claim_boundary":"This record does not claim achieved AGI, ASI, or empirical SOTA.","evidence_docket_path":"unavailable","scoreboard_path":"unavailable","artifact_names":[],"artifact_ids":[],"artifact_urls":[],"root_hash":"unavailable","source":"historical_backfill","metrics":metrics,"external_review":{"status":"not_started","attestations":"not_reported","issue_url":None},"pr_review":{"status":"not_applicable","pr_url":None},"links":{"public_page":"","experiment_page":"","run_page":"","raw_json":""}}

def _unsafe_ok(text):
    t=text.lower()
    return any(re.search(n,t) for n in NEG)

def validate_manifest(m):
    for k in ['schema_version','experiment_slug','workflow_name','claim_boundary','status']:
        if not m.get(k): raise ValueError(f'missing {k}')
    if m.get('source')!='historical_backfill' and not m.get('run_id'): raise ValueError('missing run_id')
    if m.get('source')!='historical_backfill' and m.get('workflow_name')!='historical_backfill' and not m.get('run_url'): raise ValueError('missing run_url')
    if m.get('schema_version')!='agialpha.evidence_run.v1': raise ValueError('schema_version invalid')
    text=(m.get('claim_boundary','')+' '+m.get('experiment_name','')).lower()
    for pat in UNSAFE:
        if re.search(pat,text) and not _unsafe_ok(text): raise ValueError('unsafe claim detected')
    metrics=m.get('metrics',{})
    for k in SECURITY_COUNTERS:
        if k not in metrics: raise ValueError(f'missing metric field {k}')
    if any(x in m.get('experiment_slug','') for x in ['cyber','gauntlet','omega','security']):
        for k in ['safety_incidents','policy_violations','raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','unsafe_automerge_count']:
            if k not in metrics: raise ValueError(f'missing security counter {k}')

def validate_registry(registry):
    r=Path(registry)
    runs=json.loads((r/'runs.json').read_text()) if (r/'runs.json').exists() else []
    for run in runs: validate_manifest(run)
