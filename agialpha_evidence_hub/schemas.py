from pathlib import Path
import json

def load_schema():
    return json.loads(Path('schemas/evidence_run_manifest.schema.json').read_text())
