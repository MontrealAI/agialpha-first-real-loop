import json
from pathlib import Path

def load_input(inp):
    p=Path(inp)
    if p.is_dir():
        for c in p.glob('*.json'): return json.loads(c.read_text())
        raise ValueError('no json manifest found')
    return json.loads(p.read_text())
