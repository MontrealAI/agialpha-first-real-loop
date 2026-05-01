import hashlib
import json
from pathlib import Path

WATCH_PATTERNS = [
    '.github/workflows/*.yml',
    '.github/workflows/*.yaml',
    'schemas/*.json',
    'docs/**/*',
    'agialpha_evidence_hub/**/*.py',
]


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _collect(repo_root: str) -> dict:
    root = Path(repo_root)
    files = []
    for pattern in WATCH_PATTERNS:
        files.extend([p for p in root.glob(pattern) if p.is_file()])
    files = sorted(set(files))
    rows = []
    for p in files:
        rel = str(p.relative_to(root))
        rows.append({'path': rel, 'sha256': _sha256(p.read_bytes())})
    return {'files': rows, 'catalog_hash': _sha256(json.dumps(rows, sort_keys=True).encode())}


def needed_update(registry: str, repo_root: str) -> dict:
    reg = Path(registry)
    reg.mkdir(parents=True, exist_ok=True)
    state_file = reg / 'needed_update_state.json'
    current = _collect(repo_root)
    previous = json.loads(state_file.read_text()) if state_file.exists() else {}
    needed = current.get('catalog_hash') != previous.get('catalog_hash')
    out = {
        'needed': needed,
        'previous_catalog_hash': previous.get('catalog_hash'),
        'current_catalog_hash': current.get('catalog_hash'),
        'changed_files': [r['path'] for r in current.get('files', []) if previous and r not in previous.get('files', [])],
    }
    state_file.write_text(json.dumps(current, indent=2))
    return out
