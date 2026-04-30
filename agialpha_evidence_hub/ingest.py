import json
from pathlib import Path
from .registry import load_registry, save_registry
from .validate import validate_manifest

def register_run(input_path,registry='evidence_registry/registry'):
    m=json.loads(Path(input_path).read_text())
    validate_manifest(m)
    d=load_registry(registry)
    d['runs']=[r for r in d['runs'] if r.get('run_id')!=m['run_id']] + [m]
    if not any(e.get('experiment_slug')==m['experiment_slug'] for e in d['experiments']):
        d['experiments'].append({'experiment_slug':m['experiment_slug'],'experiment_name':m.get('experiment_name',m['experiment_slug']),'claim_boundary':m.get('claim_boundary','pending')})
    save_registry(registry,d)
