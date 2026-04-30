import json
from pathlib import Path

def load_input(inp):
    p=Path(inp)
    if p.is_dir():
        for name in ['evidence-run-manifest.json','00_manifest.json']:
            c=p/name
            if c.exists(): return json.loads(c.read_text())
        found=next(iter(p.glob('*.json')),None)
        if found: return json.loads(found.read_text())
        raise ValueError('no json manifest found')
    return json.loads(p.read_text())
