import json
from pathlib import Path

FIXTURE_EXPECTATIONS = {
    "safe_docs_customer_repo": {"sovereign": "Claim Boundary Sovereign", "recommendation": "safe_to_review"},
    "workflow_permission_customer_repo": {"sovereign": "Workflow Permission Sovereign", "recommendation": "escalate"},
    "unsafe_claim_customer_repo": {"sovereign": "Claim Boundary Sovereign", "recommendation": "reject"},
    "token_overclaim_customer_repo": {"sovereign": "Token Utility Boundary Sovereign", "recommendation": "reject"},
    "secret_like_customer_repo": {"sovereign": "Secret Hygiene Sovereign", "recommendation": "human_review_required"},
    "automerge_customer_repo": {"sovereign": "Safe PR Remediation Sovereign", "recommendation": "reject"},
    "high_risk_use_customer_repo": {"sovereign": "Regulatory Boundary Sovereign", "recommendation": "reject"},
}

def list_fixtures(fixtures_dir: Path):
    return sorted([p.name for p in fixtures_dir.iterdir() if p.is_dir()])

def load_fixture(fixtures_dir: Path, name: str):
    meta = fixtures_dir / name / 'fixture.json'
    return json.loads(meta.read_text(encoding='utf-8'))
