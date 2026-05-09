
import hashlib, json
from uuid import uuid4

CLAIM = 'SecureRails webhook records are evidence pointers and do not certify security or authorize autonomous remediation.'

def normalize_webhook_payload(payload: dict, event_type: str, delivery_id: str, signature_verified: bool = True) -> dict:
    repo = payload.get('repository', {})
    sender = payload.get('sender', {})
    login = sender.get('login', 'unknown')
    login_hash = hashlib.sha256(str(login).encode('utf-8')).hexdigest()[:16]
    pr = payload.get('pull_request', {})
    wr = payload.get('workflow_run', {})
    return {
        'schema_version': 'securerails.webhook_event.v1',
        'event_id': str(uuid4()),
        'event_type': event_type,
        'delivery_id': delivery_id,
        'repository': {
            'owner': repo.get('owner', {}).get('login', ''),
            'name': repo.get('name', ''),
            'full_name': repo.get('full_name', ''),
            'visibility': repo.get('visibility', 'unknown') or 'unknown',
        },
        'sender': {'login_hash': login_hash, 'raw_login_redacted': True},
        'pull_request': {
            'number': pr.get('number'), 'head_sha': (pr.get('head') or {}).get('sha'),
            'base_sha': (pr.get('base') or {}).get('sha'), 'title_redacted': '[redacted]',
            'is_fork': ((pr.get('head') or {}).get('repo') or {}).get('fork')
        },
        'workflow_run': {
            'run_id': wr.get('id'), 'name': wr.get('name'), 'conclusion': wr.get('conclusion'),
            'artifacts_url_present': bool(wr.get('artifacts_url'))
        },
        'security': {'signature_verified': signature_verified, 'raw_secret_ingested': False, 'personal_data_minimized': True},
        'claim_boundary': CLAIM,
    }
