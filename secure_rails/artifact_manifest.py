import glob
import hashlib
import json
import os
from datetime import datetime, timezone

OPTIONAL_GLOBS = [
    'docs/secure-rails/*.md',
    'docs/secure-rails/templates/*.json',
    'secure_rails_registry/*.json',
    'docs/_generated/secure-rails/*.json',
    'docs/_generated/secure-rails/supply-chain/*.json',
    '**/evidence-run-manifest.json',
    '**/safety-ledger*.json',
    '**/*work-vault*.json',
    '**/*proofbundle*.json',
    '**/*evidence-docket*.json',
]


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(65536), b''):
            h.update(c)
    return h.hexdigest()


def build_manifest(repo_root, out_dir, workflow_name='local', workflow_run_id='local'):
    artifacts = []
    missing = []
    seen = set()
    for pattern in OPTIONAL_GLOBS:
        matches = glob.glob(os.path.join(repo_root, pattern), recursive=True)
        if not matches:
            missing.append(pattern)
        for p in matches:
            if os.path.isfile(p):
                rel = os.path.relpath(p, repo_root)
                if rel in seen:
                    continue
                seen.add(rel)
                artifacts.append({
                    'path': rel,
                    'sha256': _sha256(p),
                    'size_bytes': os.path.getsize(p),
                    'artifact_type': 'evidence',
                    'claim_boundary_present': True,
                })

    m = {
        'schema_version': 'securerails.artifact_manifest.v1',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'repository': os.getenv('GITHUB_REPOSITORY', 'MontrealAI/agialpha-first-real-loop'),
        'commit_sha': os.getenv('GITHUB_SHA', 'local'),
        'workflow_run_id': str(workflow_run_id),
        'workflow_name': workflow_name,
        'artifact_scope': 'secure_rails_supply_chain_provenance_001',
        'artifacts': sorted(artifacts, key=lambda x: x['path']),
        'not_found': missing,
        'claim_boundary': 'This artifact manifest records hashes and provenance metadata. It does not certify security or claim empirical SOTA.',
    }

    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, 'artifact_manifest.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(m, f, indent=2)
    return m
