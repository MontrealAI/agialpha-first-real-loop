import json
from pathlib import Path

DECISIONS={"accept","reject","escalate","request_changes","archive_only"}
TARGETS={"none","safe_pr","capability_archive","release","policy_update","customer_pilot_status"}

def validate_review_decision(record: dict) -> list[str]:
    errs=[]
    if record.get("schema_version")!="securerails.human_review_decision.v1": errs.append("invalid schema_version")
    if not isinstance(record.get("decision_id"), str) or not record.get("decision_id", "").strip(): errs.append("decision_id required")
    if record.get("decision") not in DECISIONS: errs.append("invalid decision")
    if not str(record.get("decision_summary"," ")).strip(): errs.append("decision_summary required")
    if not str(record.get("claim_boundary"," ")).strip(): errs.append("claim_boundary required")
    promo=record.get("promotion",{})
    if promo.get("promotion_target") not in TARGETS: errs.append("invalid promotion_target")
    if promo.get("auto_merge_allowed") is not False: errs.append("auto_merge_allowed must be false")
    if promo.get("promotion_target")=="safe_pr" and promo.get("manual_merge_required") is not True: errs.append("manual_merge_required must be true for safe_pr")
    evidence=record.get("evidence_reviewed",{})
    if not isinstance(evidence, dict):
        errs.append("evidence_reviewed must be an object")
        evidence = {}
    if promo.get("promotion_allowed") is True:
        for k in ["evidence_docket_reviewed","safety_ledger_reviewed","claim_boundary_reviewed"]:
            if evidence.get(k) is not True: errs.append(f"{k} must be true when promotion_allowed")
    counters=record.get("hard_safety_counters")
    if not isinstance(counters,dict): errs.append("hard_safety_counters required")
    return errs

def load_and_validate_decision(path: Path) -> list[str]:
    return validate_review_decision(json.loads(path.read_text(encoding="utf-8")))
