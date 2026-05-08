import json
from pathlib import Path
from .pilot_models import REQUIRED_CLAIM_BOUNDARY, FORBIDDEN_UTILITY_TERMS, ValidationResult

def _req(obj, path):
    cur = obj
    for p in path.split('.'):
        if not isinstance(cur, dict):
            return None
        if p not in cur:
            return None
        cur = cur[p]
    return cur

def validate_intake_record(rec: dict) -> ValidationResult:
    e = []

    required_identity = [
        "pilot_id", "customer_label", "repo.provider", "repo.owner", "repo.name", "repo.repo_url", "source.ingestion_method"
    ]
    for f in required_identity:
        v = _req(rec, f)
        if v in (None, ""):
            e.append(f"{f} missing")
    checks_false = [
        "scope.external_target_scanning_allowed","scope.exploit_execution_allowed","scope.malware_generation_allowed",
        "scope.social_engineering_allowed","scope.auto_merge_allowed","scope.hr_worker_evaluation_allowed",
        "scope.profiling_natural_persons_allowed","scope.automated_decisions_about_natural_persons_allowed",
        "scope.critical_infrastructure_safety_component_reliance_allowed","privacy.raw_customer_secrets_ingested"
    ]
    checks_true = ["scope.repo_owned","scope.defensive_only","scope.human_review_required"]
    for c in checks_true:
        if _req(rec,c) is not True: e.append(f"{c} must be true")
    for c in checks_false:
        if _req(rec,c) is not False: e.append(f"{c} must be false")
    if not rec.get("claim_boundary"): e.append("claim_boundary missing")
    if rec.get("claim_boundary") != REQUIRED_CLAIM_BOUNDARY: e.append("claim_boundary mismatch")
    if "hard_safety_counters" not in rec: e.append("hard_safety_counters missing")
    ua = json.dumps(rec.get("utility_accounting", {})).lower()
    for t in FORBIDDEN_UTILITY_TERMS:
        if t in ua: e.append(f"forbidden utility term: {t}")
    return ValidationResult(ok=not e, errors=e)

def validate_intake_file(path: Path) -> ValidationResult:
    return validate_intake_record(json.loads(path.read_text(encoding='utf-8')))
