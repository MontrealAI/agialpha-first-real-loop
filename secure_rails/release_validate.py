from pathlib import Path
import json
import hashlib
from .release_manifest import validate_manifest

def validate_bundle(inp:Path):
 manifest_path = inp / 'release_manifest.json'
 if not manifest_path.exists():
  raise ValueError('release_manifest.json missing')
 m=json.loads(manifest_path.read_text());ok,errs=validate_manifest(m)
 if not ok: raise ValueError('; '.join(errs))
 required = ['CHECKSUMS.sha256', 'artifact_manifest.json', 'RELEASE_NOTES.md', 'CUSTOMER_INSTALL.md', 'MARKETPLACE_READINESS.md']
 missing = [name for name in required if not (inp / name).exists()]
 if missing:
  raise ValueError('missing bundle files: ' + ', '.join(missing))
 artifact_manifest = json.loads((inp / 'artifact_manifest.json').read_text(encoding='utf-8'))
 artifacts = artifact_manifest.get('artifacts', [])
 if not isinstance(artifacts, list) or not artifacts:
  raise ValueError('artifact_manifest.json has no artifacts list')
 for rel in artifacts:
  if not (inp / rel).exists():
    raise ValueError(f'artifact listed but missing: {rel}')
 checksum_lines = [ln.strip() for ln in (inp / 'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines() if ln.strip()]
 checksum_map = {}
 for ln in checksum_lines:
  parts = ln.split('  ', 1)
  if len(parts) != 2:
    raise ValueError(f'invalid checksum line: {ln}')
  checksum_map[parts[1]] = parts[0]
 if 'artifact_manifest.json' not in checksum_map:
  raise ValueError('artifact_manifest.json missing from checksums')
 for rel, expected in checksum_map.items():
  p = inp / rel
  if not p.exists():
    raise ValueError(f'checksum file entry missing on disk: {rel}')
  got = hashlib.sha256(p.read_bytes()).hexdigest()
  if got != expected:
    raise ValueError(f'checksum mismatch: {rel}')
