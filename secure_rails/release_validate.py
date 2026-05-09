from pathlib import Path
import json
from .release_manifest import validate_manifest

def validate_bundle(inp:Path):
 m=json.loads((inp/'release_manifest.json').read_text());ok,errs=validate_manifest(m)
 if not ok: raise ValueError('; '.join(errs))
