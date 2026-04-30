import json
from pathlib import Path
from datetime import datetime

def _r(p,d): return json.loads(p.read_text()) if p.exists() else d

def ensure_structure(registry):
    r=Path(registry); r.mkdir(parents=True,exist_ok=True)
    for d in ['experiments','workflows','indexes','raw']: (r/d).mkdir(exist_ok=True)
    for f,default in [('runs.json',[]),('experiments.json',[]),('workflows.json',[]),('latest.json',{}),('registry.json',{})]:
        p=r/f
        if not p.exists(): p.write_text(json.dumps(default,indent=2))
    ch=r/'CHANGELOG.md'
    if not ch.exists(): ch.write_text('# Evidence Registry Changelog\n')

def update_indexes(runs,registry):
    r=Path(registry)
    by_status={}; by_workflow={}; by_family={}; by_claim={}
    for x in runs:
        by_status.setdefault(x.get('status','unknown'),[]).append(x['run_id'])
        by_workflow.setdefault(x.get('workflow_name','unknown'),[]).append(x['run_id'])
        by_family.setdefault(x.get('experiment_family','other'),[]).append(x['run_id'])
        by_claim.setdefault(x.get('claim_level','pending'),[]).append(x['run_id'])
    (r/'indexes/by_status.json').write_text(json.dumps(by_status,indent=2))
    (r/'indexes/by_workflow.json').write_text(json.dumps(by_workflow,indent=2))
    (r/'indexes/by_family.json').write_text(json.dumps(by_family,indent=2))
    (r/'indexes/by_claim_level.json').write_text(json.dumps(by_claim,indent=2))
    (r/'indexes/by_date.json').write_text(json.dumps(sorted([x.get('generated_at','') for x in runs],reverse=True),indent=2))

def register(manifest, registry='evidence_registry'):
    ensure_structure(registry)
    r=Path(registry)
    runs=_r(r/'runs.json',[])
    rid=manifest.get('run_id') or f"historical-{manifest.get('experiment_slug','unknown')}"
    manifest['run_id']=rid
    old=next((x for x in runs if x.get('run_id')==rid),None)
    runs=[x for x in runs if x.get('run_id')!=rid]+[manifest]
    runs=sorted(runs,key=lambda x:x.get('generated_at',''),reverse=True)
    (r/'runs.json').write_text(json.dumps(runs,indent=2))
    exps=sorted(set([x.get('experiment_slug','unknown') for x in runs])); (r/'experiments.json').write_text(json.dumps(exps,indent=2))
    wfs=sorted(set([x.get('workflow_name','unknown') for x in runs])); (r/'workflows.json').write_text(json.dumps(wfs,indent=2))
    (r/'latest.json').write_text(json.dumps(runs[0] if runs else {},indent=2))
    exp=manifest.get('experiment_slug','unknown'); ep=r/'experiments'/exp; (ep/'runs').mkdir(parents=True,exist_ok=True)
    (ep/'runs'/f"{rid}.json").write_text(json.dumps(manifest,indent=2))
    (ep/'experiment.json').write_text(json.dumps({'experiment_slug':exp},indent=2)); (ep/'latest.json').write_text(json.dumps(manifest,indent=2))
    update_indexes(runs,registry)
    with (r/'CHANGELOG.md').open('a') as f:
        f.write(f"- {datetime.utcnow().isoformat()}Z run_id={rid} experiment={exp} source={manifest.get('source','unknown')} updated_fields={','.join(sorted(manifest.keys()))}\n")
    return manifest
