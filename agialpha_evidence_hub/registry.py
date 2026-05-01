import json
from pathlib import Path
from datetime import datetime, timezone

def _read(path, default):
    return json.loads(path.read_text()) if path.exists() else default

def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=False))

def load_registry(base='evidence_registry'):
    b=Path(base)
    return {
      'runs': _read(b/'runs.json', []),
      'experiments': _read(b/'experiments.json', []),
      'workflows': _read(b/'workflows.json', []),
    }

def save_registry(base, data):
    b=Path(base)
    runs=sorted(data['runs'], key=lambda r:r.get('generated_at',''), reverse=True)
    _write(b/'runs.json', runs)
    _write(b/'experiments.json', sorted(data['experiments'], key=lambda x:x['slug']))
    _write(b/'workflows.json', sorted(data['workflows'], key=lambda x:x['slug']))
    _write(b/'latest.json', runs[0] if runs else {})
    _write(b/'registry.json', {'run_count':len(runs),'experiment_count':len(data['experiments']),'workflow_count':len(data['workflows'])})

def update_registry(base, manifest):
    reg=load_registry(base)
    run_id=manifest.get('run_id') or f"historical-{manifest.get('experiment_slug','unknown')}"
    manifest['run_id']=run_id
    existing=next((r for r in reg['runs'] if r.get('run_id')==run_id), None)
    if existing:
        merged=dict(existing)
        merged.update({k:v for k,v in manifest.items() if v not in (None,'',[],{},'unavailable','not_reported')})
        old_metrics=existing.get('metrics',{}) if isinstance(existing.get('metrics',{}),dict) else {}
        new_metrics=manifest.get('metrics',{}) if isinstance(manifest.get('metrics',{}),dict) else {}
        metrics=dict(old_metrics)
        for k,v in new_metrics.items():
            if k not in metrics or metrics.get(k) in (None,'','unavailable','not_reported'):
                metrics[k]=v
        merged['metrics']=metrics
        manifest=merged
    reg['runs']=[r for r in reg['runs'] if r.get('run_id')!=run_id]+[manifest]
    exp={'slug':manifest.get('experiment_slug','unknown'),'name':manifest.get('experiment_name',manifest.get('experiment_slug','unknown')),'family':manifest.get('experiment_family','other')}
    if exp['slug'] not in [e['slug'] for e in reg['experiments']]: reg['experiments'].append(exp)
    wslug=manifest.get('workflow_name','unknown').lower().replace(' ','-')
    w={'slug':wslug,'name':manifest.get('workflow_name','unknown'),'workflow_file':manifest.get('workflow_file','unknown')}
    if w['slug'] not in [x['slug'] for x in reg['workflows']]: reg['workflows'].append(w)
    save_registry(base, reg)
    cl=Path(base)/'CHANGELOG.md'
    ts=datetime.now(timezone.utc).isoformat()
    cl.parent.mkdir(parents=True,exist_ok=True)
    prev=cl.read_text() if cl.exists() else '# Evidence Registry Changelog\n\n'
    cl.write_text(prev+f"- {ts} run_id={run_id} experiment={manifest.get('experiment_slug')} source={manifest.get('source','manifest')}\n")
