import json
from .policy_rules import load_rules
from .policy_decision import make_decision

HARD_TERMS = {"reject": "critical", "quarantine": "critical", "escalate": "high", "warn":"low", "allow":"info"}

def load_kernel(path):
    from pathlib import Path
    return json.loads(Path(path).read_text(encoding='utf-8'))

def validate_kernel(kernel):
    errs=[]
    if kernel.get("human_review_required") is not True: errs.append("human_review_required must be true")
    if kernel.get("autonomous_promotion_allowed") is not False: errs.append("autonomous_promotion_allowed must be false")
    if kernel.get("auto_merge_allowed") is not False: errs.append("auto_merge_allowed must be false")
    if not kernel.get("claim_boundary"): errs.append("claim_boundary missing")
    if kernel.get("default_decision") == "allow": errs.append("default_decision cannot be allow")
    return errs

def evaluate_context(context, kernel, rules):
    hay = "\n".join(context.get("text_fields", [])).lower() + "\n" + json.dumps(context.get("content", {})).lower()
    decision = kernel.get("default_decision", "escalate")
    matched=[];viol=[];warn=[]

    domain_context_map = {
        'work_vault':'work_vault',
        'mark_allocation':'mark_allocation',
        'sovereign':'sovereign',
        'github_app_connector':'github_app',
        'release_train':'release',
        'trust_center':'trust_center',
        'repo_security_baseline':'repo_security',
    }
    negations=['does not claim achieved agi','not empirical sota','not cybersecurity certification','does not certify security']
    for r in rules:
        target = domain_context_map.get(r.get('domain'))
        if target and context.get('context_type') != target:
            continue
        forbidden_hit=any(t.lower() in hay for t in r.get('forbidden_terms', []))
        if r.get('domain') == 'claim_boundary' and forbidden_hit and any(n in hay for n in negations):
            forbidden_hit=False
        if forbidden_hit:
            matched.append(r["rule_id"]);viol.append(r["message"])
            if r.get("decision") in ["reject","quarantine"]: decision = r["decision"]
            elif decision not in ["reject","quarantine"]: decision = r.get("decision", decision)
        if all(t.lower() in hay for t in r.get("required_terms", [])) is False and r.get("required_terms"):
            matched.append(r["rule_id"]);viol.append("missing required terms: " + ",".join(r["required_terms"]))
            if r.get("missing_decision"): decision = r["missing_decision"]
    # allow negated boundary phrases
    if "does not claim achieved agi" in hay or "not empirical sota" in hay:
        if decision == "escalate": decision = "allow"
    sev = HARD_TERMS.get(decision, "medium")
    return make_decision(context, kernel, decision, sev, matched, viol, warn)


def evaluate_file(input_path, context_type="auto", kernel_path="config/securerails_policy_kernel.json"):
    from .policy_context import build_context
    kernel=load_kernel(kernel_path)
    rules=load_rules()
    return evaluate_context(build_context(input_path, context_type), kernel, rules)
