import json
from pathlib import Path

REQUEST_TYPES={"work_vault","safe_pr","policy_decision","customer_pilot","release_candidate","repo_security_baseline","trust_center","generic"}
REQUESTED_DECISIONS={"accept","reject","escalate","request_changes","archive_only"}
RISK_TIERS={"low","medium","high","critical"}

def validate_review_request(record: dict) -> list[str]:
    errs=[]
    if record.get("schema_version")!="securerails.human_review_request.v1": errs.append("invalid schema_version")
    if record.get("request_type") not in REQUEST_TYPES: errs.append("invalid request_type")
    if record.get("requested_decision") not in REQUESTED_DECISIONS: errs.append("invalid requested_decision")
    if record.get("risk_tier") not in RISK_TIERS: errs.append("invalid risk_tier")
    if record.get("human_review_required") is not True: errs.append("human_review_required must be true")
    if record.get("auto_merge_allowed") is not False: errs.append("auto_merge_allowed must be false")
    if not str(record.get("claim_boundary"," ")).strip(): errs.append("claim_boundary required")
    src=record.get("source",{})
    refs=[src.get(k) for k in ["work_vault_id","mark_allocation_id","sovereign_id","proofbundle_id","evidence_docket_id","policy_decision_id","pull_request_url","artifact_url"]]
    if not any(v not in (None,"") for v in refs): errs.append("source must include at least one reference")
    return errs

def load_and_validate_request(path: Path) -> list[str]:
    return validate_review_request(json.loads(path.read_text(encoding="utf-8")))
