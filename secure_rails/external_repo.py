import json
from pathlib import Path
from typing import Any, Dict, List


def load_external_repo_config(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def _repo_url(provider: str, owner: str, name: str) -> str:
    if provider == 'github':
        return f'https://github.com/{owner}/{name}'
    return ''


def _record_from_repo(repo: Dict[str, Any]) -> Dict[str, Any]:
    owner = repo.get('owner', 'unknown-owner')
    name = repo.get('name', 'unknown-repo')
    provider = repo.get('provider', 'github')
    return {
        'schema_version': 'securerails.customer_pilot_intake.v1',
        'pilot_id': f'sr-pilot-sync-{provider}-{owner}-{name}',
        'customer_label': repo.get('customer_label', 'design-partner-redacted'),
        'customer_public_name': None,
        'repo': {
            'provider': provider,
            'owner': owner,
            'name': name,
            'visibility': repo.get('visibility', 'unknown'),
            'repo_url': _repo_url(provider, owner, name),
        },
        'source': {
            'ingestion_method': 'artifact_api',
            'workflow_run_id': None,
            'artifact_id': None,
            'artifact_name': repo.get('artifact_name', 'not_reported'),
            'artifact_digest': 'not_reported',
            'artifact_url': None,
            'artifact_status': 'pending' if repo.get('allow_artifact_api', False) else 'unavailable',
        },
        'scope': {
            'repo_owned': True,
            'defensive_only': True,
            'human_review_required': True,
            'external_target_scanning_allowed': False,
            'exploit_execution_allowed': False,
            'malware_generation_allowed': False,
            'social_engineering_allowed': False,
            'auto_merge_allowed': False,
            'hr_worker_evaluation_allowed': False,
            'profiling_natural_persons_allowed': False,
            'automated_decisions_about_natural_persons_allowed': False,
            'critical_infrastructure_safety_component_reliance_allowed': False,
        },
        'evidence': {'human_review_status': 'pending', 'recommendation': 'human_review_required'},
        'hard_safety_counters': {
            'raw_secret_leak_count': 0,
            'external_target_scan_count': 0,
            'exploit_execution_count': 0,
            'malware_generation_count': 0,
            'social_engineering_content_count': 0,
            'unsafe_automerge_count': 0,
            'critical_safety_incidents': 0,
        },
        'privacy': {
            'raw_customer_secrets_ingested': False,
            'personal_data_intended': False,
            'redaction_required': True,
            'public_display_allowed': False,
        },
        'utility_accounting': {
            'asset': '$AGIALPHA',
            'mode': 'mock',
            'alpha_work_units': 'not_reported',
            'settlement_status': 'recorded_not_financial_settlement',
        },
        'status': 'pending_validation',
        'claim_boundary': 'SecureRails customer pilot intake records are evidence-governance artifacts. They do not certify security, do not authorize autonomous remediation, and do not make decisions about natural persons.',
    }


def sync_external_repos(config_path: Path, limit: int) -> List[Dict[str, Any]]:
    cfg = load_external_repo_config(config_path)
    repos = cfg.get('repos', [])
    return [_record_from_repo(repo) for repo in repos[: max(0, limit)]]
