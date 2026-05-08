import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def _headers():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers, bool(token)


def _get_json(url: str, headers: dict):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def load_external_repo_config(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def build_sync_intakes(config_path: Path, limit: int = 20):
    cfg = load_external_repo_config(config_path)
    repos = cfg.get("repos", [])[: max(limit, 0)]
    headers, has_token = _headers()
    out = []
    for repo in repos:
        owner = repo.get("owner", "unknown")
        name = repo.get("name", "unknown")
        pilot_id = f"sr-pilot-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{owner}-{name}".replace("_", "-")
        artifact_name = repo.get("artifact_name", "securerails-pr-guard-output")
        artifact_status = "unavailable"
        workflow_run_id = None
        artifact_id = None
        artifact_url = None
        artifact_digest = "not_reported"

        if repo.get("allow_artifact_api", False):
            if has_token:
                try:
                    base = f"https://api.github.com/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(name)}"
                    data = _get_json(f"{base}/actions/artifacts?per_page=20", headers)
                    artifacts = data.get("artifacts", [])
                    match = next((a for a in artifacts if a.get("name") == artifact_name), artifacts[0] if artifacts else None)
                    if match:
                        artifact_id = match.get("id")
                        artifact_url = match.get("archive_download_url")
                        artifact_status = "expired" if match.get("expired") else "available"
                        workflow_run_id = str(match.get("workflow_run", {}).get("id")) if match.get("workflow_run") else None
                except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
                    artifact_status = "unavailable"
            else:
                artifact_status = "pending"

        out.append({
            "schema_version": "securerails.customer_pilot_intake.v1",
            "pilot_id": pilot_id,
            "customer_label": repo.get("customer_label", "design-partner-redacted"),
            "customer_public_name": None,
            "repo": {
                "provider": "github",
                "owner": owner,
                "name": name,
                "visibility": repo.get("visibility", "unknown"),
                "repo_url": f"https://github.com/{owner}/{name}",
            },
            "source": {
                "ingestion_method": "artifact_api",
                "workflow_run_id": workflow_run_id,
                "artifact_id": str(artifact_id) if artifact_id is not None else None,
                "artifact_name": artifact_name,
                "artifact_digest": artifact_digest,
                "artifact_url": artifact_url,
                "artifact_status": artifact_status,
            },
            "scope": {
                "repo_owned": True, "defensive_only": True, "human_review_required": True,
                "external_target_scanning_allowed": False, "exploit_execution_allowed": False, "malware_generation_allowed": False,
                "social_engineering_allowed": False, "auto_merge_allowed": False, "hr_worker_evaluation_allowed": False,
                "profiling_natural_persons_allowed": False, "automated_decisions_about_natural_persons_allowed": False,
                "critical_infrastructure_safety_component_reliance_allowed": False,
            },
            "evidence": {"human_review_status": "pending", "recommendation": "human_review_required"},
            "hard_safety_counters": {
                "raw_secret_leak_count": 0, "external_target_scan_count": 0, "exploit_execution_count": 0,
                "malware_generation_count": 0, "social_engineering_content_count": 0, "unsafe_automerge_count": 0,
                "critical_safety_incidents": 0,
            },
            "privacy": {"raw_customer_secrets_ingested": False, "personal_data_intended": False, "redaction_required": True, "public_display_allowed": False},
            "utility_accounting": {"asset": "$AGIALPHA", "mode": "mock", "alpha_work_units": "not_reported", "settlement_status": "recorded_not_financial_settlement"},
            "status": "pending_validation",
            "claim_boundary": "SecureRails customer pilot intake records are evidence-governance artifacts. They do not certify security, do not authorize autonomous remediation, and do not make decisions about natural persons.",
        })
    return out
