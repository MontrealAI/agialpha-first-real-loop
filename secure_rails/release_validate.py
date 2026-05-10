from pathlib import Path
import json
import hashlib
from .release_manifest import validate_manifest

REQUIRED_FILES = [
    'release_manifest.json',
    'RELEASE_NOTES.md',
    'CLAIM_BOUNDARY.md',
    'CUSTOMER_INSTALL.md',
    'MARKETPLACE_READINESS.md',
    'CHECKSUMS.sha256',
    'artifact_manifest.json',
]

def _sha(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def validate_bundle(inp:Path):
 missing = [f for f in REQUIRED_FILES if not (inp / f).exists()]
 if missing:
  raise ValueError('missing required bundle files: ' + ', '.join(missing))
 m=json.loads((inp/'release_manifest.json').read_text());ok,errs=validate_manifest(m)
 if not ok: raise ValueError('; '.join(errs))
 artifact_manifest = json.loads((inp / 'artifact_manifest.json').read_text(encoding='utf-8'))
 artifacts = artifact_manifest.get('artifacts', [])
 for rel in artifacts:
  if not (inp / rel).exists():
    raise ValueError(f'artifact listed but missing: {rel}')
 checksums = (inp / 'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
 mapping = {}
 for line in checksums:
  if '  ' not in line:
    continue
  digest, rel = line.split('  ', 1)
  mapping[rel.strip()] = digest.strip()
 for rel in artifacts + ['artifact_manifest.json']:
  p = inp / rel
  if p.exists():
    actual = _sha(p)
    expected = mapping.get(rel)
    if expected != actual:
      raise ValueError(f'checksum mismatch or missing entry: {rel}')
