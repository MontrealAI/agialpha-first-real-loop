import json
from pathlib import Path

def _read(p,d): return json.loads(p.read_text()) if p.exists() else d

def register(manifest, registry='evidence_registry/registry'):
    r=Path(registry); r.mkdir(parents=True,exist_ok=True)
    runs=_read(r/'runs.json',[]); exps=_read(r/'experiments.json',[])
    runs=[x for x in runs if x.get('run_id')!=manifest['run_id']]+[manifest]
    runs=sorted(runs,key=lambda x:x.get('generated_at',''),reverse=True)
    slug=manifest['experiment_slug']
    if slug not in exps: exps.append(slug)
    (r/'runs.json').write_text(json.dumps(runs,indent=2))
    (r/'experiments.json').write_text(json.dumps(sorted(exps),indent=2))
    (r/'latest.json').write_text(json.dumps(runs[0] if runs else {},indent=2))
