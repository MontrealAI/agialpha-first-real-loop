import json
from pathlib import Path

def load_schema(path: str = 'schemas/evidence_run_manifest.schema.json'):
    return json.loads(Path(path).read_text())
