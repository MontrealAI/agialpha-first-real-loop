import hashlib
import json
import os
from datetime import datetime, timezone


def _workflow_run_url() -> str:
    repo = os.getenv('GITHUB_REPOSITORY', 'MontrealAI/agialpha-first-real-loop')
    run_id = os.getenv('GITHUB_RUN_ID', '0')
    return f"https://github.com/{repo}/actions/runs/{run_id}"


def build_provenance(repo_root, manifest_path, out_path):
    with open(manifest_path, 'rb') as f:
        data = f.read()

    attestation_status = 'not_attempted' if os.getenv('GITHUB_ACTIONS') else 'unavailable'
    attestation_reason = 'local run' if not os.getenv('GITHUB_ACTIONS') else 'skipped by input'

    rec = {
        'schema_version': 'securerails.provenance_record.v1',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'repository': os.getenv('GITHUB_REPOSITORY', 'MontrealAI/agialpha-first-real-loop'),
        'commit_sha': os.getenv('GITHUB_SHA', 'local'),
        'branch': os.getenv('GITHUB_REF_NAME', 'local'),
        'workflow_name': os.getenv('GITHUB_WORKFLOW', 'local'),
        'workflow_file': '.github/workflows/securerails-supply-chain-provenance-001.yml',
        'workflow_run_id': os.getenv('GITHUB_RUN_ID', 'local'),
        'workflow_run_url': _workflow_run_url(),
        'event_name': os.getenv('GITHUB_EVENT_NAME', 'local'),
        'actor': os.getenv('GITHUB_ACTOR', 'local'),
        'artifact_manifest_sha256': hashlib.sha256(data).hexdigest(),
        'builder': {
            'type': 'github_actions' if os.getenv('GITHUB_ACTIONS') else 'local',
            'runner': os.getenv('RUNNER_NAME', 'local'),
            'permissions_summary': {},
        },
        'attestation': {
            'status': attestation_status,
            'method': 'local_provenance_record',
            'attestation_paths': [],
            'verification_instructions': f'Use sha256sum and compare hashes against artifact_manifest.json ({attestation_reason}).',
        },
        'claim_boundary': 'This provenance record documents where and how artifacts were produced. It is not a security certification.',
    }

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(rec, f, indent=2)

    return rec
