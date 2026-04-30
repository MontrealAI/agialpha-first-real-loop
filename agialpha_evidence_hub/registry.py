import json
from pathlib import Path

def load_registry(reg):
    p=Path(reg)
    runs=json.loads((p/'runs.json').read_text()) if (p/'runs.json').exists() else []
    exps=json.loads((p/'experiments.json').read_text()) if (p/'experiments.json').exists() else []
    wfs=json.loads((p/'workflows.json').read_text()) if (p/'workflows.json').exists() else []
    return {'runs':runs,'experiments':exps,'workflows':wfs}

def save_registry(reg,data):
    p=Path(reg);p.mkdir(parents=True,exist_ok=True)
    for k in ['runs','experiments','workflows']:
        (p/f'{k}.json').write_text(json.dumps(data.get(k,[]),indent=2))
