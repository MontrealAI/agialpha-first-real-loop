import json
from pathlib import Path
from .pilot_validate import validate_intake_record
from .pilot_registry import add_record

def ingest_intake(input_path: Path, registry: Path):
    rec=json.loads(input_path.read_text(encoding='utf-8'))
    vr=validate_intake_record(rec)
    rec['status']='validated' if vr.ok else 'quarantined'
    rec['validation_errors']=vr.errors
    add_record(registry, rec)
    return rec
