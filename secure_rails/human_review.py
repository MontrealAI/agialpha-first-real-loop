import json
from pathlib import Path
from .review_request import validate_review_request
from .review_decision import validate_review_decision

PROMOTION_TARGETS = {"safe_pr", "capability_archive", "release", "policy_update", "customer_pilot_status"}

def validate_promotion_gate(record: dict) -> list[str]:
    errs=[]
    if record.get("schema_version")!="securerails.promotion_gate.v1": errs.append("invalid schema_version")
    if not isinstance(record.get("promotion_gate_id"), str) or not record.get("promotion_gate_id", "").strip(): errs.append("promotion_gate_id required")
    source_decision_id = record.get("source_decision_id")
    if not isinstance(source_decision_id, str) or not source_decision_id.strip(): errs.append("source_decision_id required")
    if record.get("promotion_target") not in PROMOTION_TARGETS: errs.append("invalid promotion_target")
    cond=record.get("required_conditions",{})
    if not isinstance(cond, dict):
        errs.append("required_conditions must be an object")
        return errs
    if cond.get("human_review_decision_present") is not True: errs.append("human_review_decision_present must be true")
    if cond.get("hard_safety_counters_zero") is not True: errs.append("hard_safety_counters_zero must be true")
    if cond.get("auto_merge_allowed") is not False: errs.append("auto_merge_allowed must be false")
    if not str(record.get("claim_boundary"," ")).strip(): errs.append("claim_boundary required")
    if record.get("promotion_target") in PROMOTION_TARGETS and cond.get("evidence_docket_present") is not True:
        errs.append("evidence_docket_present must be true")
    return errs

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
