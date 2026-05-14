import json
from pathlib import Path

def jwrite(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")

def jread(path, default):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text())
