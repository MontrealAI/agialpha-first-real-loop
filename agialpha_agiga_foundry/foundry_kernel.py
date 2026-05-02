import json
from pathlib import Path

def load_kernel(path):
    return json.loads(Path(path).read_text())
