import json
from pathlib import Path

def load_external_repo_config(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))
