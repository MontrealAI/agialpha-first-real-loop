from pathlib import Path
import json

def extract_index(run_dir):
    p=Path(run_dir)
    files=[str(x.relative_to(p)) for x in p.rglob('*') if x.is_file()]
    return {'files':files}

def save_index(run_dir,out):
    Path(out).write_text(json.dumps(extract_index(run_dir),indent=2))
