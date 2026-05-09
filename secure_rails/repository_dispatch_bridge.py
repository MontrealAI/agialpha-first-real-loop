
import json
from pathlib import Path

ALLOWED_EVENT_TYPES = {'securerails_customer_pilot_completed'}
CLAIM = 'This dispatch is a pointer to SecureRails evidence artifacts, not a security certification.'

def build_dispatch_from_webhook_event(event: dict) -> dict:
    security = event.get('security', {})
    if security.get('signature_verified') is not True:
        raise ValueError('webhook event signature must be verified before dispatch build')
    if event.get('event_type') != 'workflow_run':
        raise ValueError('dispatch build requires workflow_run event type')
    workflow_run = event.get('workflow_run', {})
    if workflow_run.get('conclusion') != 'success':
        raise ValueError('dispatch build requires successful workflow_run conclusion')
    if workflow_run.get('run_id') in (None, '', 'not_reported'):
        raise ValueError('dispatch build requires workflow_run.run_id')
    repo = event.get('repository', {}).get('full_name', '')
    wrid = workflow_run.get('run_id')
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
    cp=data.get('client_payload',{})
    sensitive_keys={'token','password','secret','api_key','authorization'}
    bad_keys=[k for k in cp.keys() if str(k).lower() in sensitive_keys]
    if bad_keys: e.append('secret-like field detected')
    return (len(e)==0,e)
