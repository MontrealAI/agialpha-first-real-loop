
import json
from pathlib import Path

ALLOWED_EVENT_TYPES = {'securerails_customer_pilot_completed'}
CLAIM = 'This dispatch is a pointer to SecureRails evidence artifacts, not a security certification.'

def build_dispatch_from_webhook_event(event: dict) -> dict:
    repo = event.get('repository', {}).get('full_name', '')
    wrid = event.get('workflow_run', {}).get('run_id', 'not_reported')
    return {
        'schema_version': 'securerails.repository_dispatch_bridge.v1',
        'event_type': 'securerails_customer_pilot_completed',
        'client_payload': {
            'pilot_id': event.get('event_id', ''), 'repo': repo, 'workflow_run_id': str(wrid),
            'artifact_name': 'securerails-pr-guard-output', 'artifact_digest': 'not_reported',
            'public_display_allowed': False, 'human_review_required': True, 'claim_boundary': CLAIM
        }
    }

def validate_dispatch_payload(data: dict) -> tuple[bool, list[str]]:
    e=[]
    if data.get('event_type') not in ALLOWED_EVENT_TYPES: e.append('event_type not allowed')
    cp=data.get('client_payload',{})
    if cp.get('public_display_allowed', False) is not False: e.append('public_display_allowed must default false')
    if cp.get('human_review_required') is not True: e.append('human_review_required must be true')
    if 'claim_boundary' not in cp: e.append('claim_boundary missing')
    s=json.dumps(data).lower()
    for bad in ['token','password','secret']:
        if bad in s: e.append('secret-like field detected'); break
    return (len(e)==0,e)
