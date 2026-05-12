import json
from pathlib import Path
from .policy_rules import load_rules
from .policy_decision import make_decision

HARD_TERMS = {"reject": "critical", "quarantine": "critical", "escalate": "high", "warn":"low", "allow":"info"}

def load_kernel(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _all_required_terms_present(context, required_terms):
    if not required_terms:
        return True
    hay = "\n".join(context.get("text_fields", [])).lower() + "\n" + json.dumps(context.get("content", {})).lower()
    return all(t.lower() in hay for t in required_terms)


def _required_keys_present(content, required_terms):
    if not isinstance(content, dict):
        return False
    return all(k in content for k in required_terms)


def _work_vault_flags_true(content, required_terms):
    if not isinstance(content, dict):
        return False
    required = {t for t in required_terms if t in {"human_review_required", "defensive_only", "repo_owned"}}
    if not required:
        return True
    return all(content.get(flag) is True for flag in required)



def _claim_forbidden_hit(hay: str, forbidden_terms):
    safe_phrases = [
        'does not claim achieved agi',
        'does not claim achieved asi',
        'not empirical sota',
        'is not empirical sota',
        'not cybersecurity certification',
        'does not certify security',
        'not guaranteed security',
        'not eu ai act exempt',
        'no investment return',
        'no token appreciation',
        'no yield',
        'no dividends',
        'no profit rights',
        'no ownership rights',
    ]
    for term in forbidden_terms:
        t = term.lower()
        if t not in hay:
            continue
        total_hits = hay.count(t)
        safe_hits = sum(hay.count(phrase) for phrase in safe_phrases if t in phrase)
        if total_hits > safe_hits:
            return True
    return False

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

    domain_context = {
        'claim_boundary': {'generic_text','pull_request','release','trust_center','repo_security','customer_pilot','github_app','work_vault','mark_allocation','sovereign'},
        'safety_boundary': {'generic_text','pull_request','work_vault','mark_allocation','sovereign'},
        'eu_ai_act_boundary': {'generic_text','customer_pilot','pull_request'},
        'token_utility_boundary': {'generic_text','mark_allocation','sovereign','release'},
        'work_vault': {'work_vault'},
        'github_app_connector': {'github_app'},
        'release_train': {'release'},
        'trust_center': {'trust_center'},
        'repo_security_baseline': {'repo_security'},
        'mark_allocation': {'mark_allocation'},
        'sovereign': {'sovereign'},
    }
    for r in rules:
        allowed_contexts = domain_context.get(r.get('domain'), {context.get('context_type')})
        if context.get('context_type') not in allowed_contexts:
            continue
        if r.get('domain') == 'claim_boundary':
            forbidden_hit = _claim_forbidden_hit(hay, r.get('forbidden_terms', []))
        else:
            forbidden_hit=any(t.lower() in hay for t in r.get('forbidden_terms', []))
        if forbidden_hit:
            matched.append(r["rule_id"]);viol.append(r["message"])
            if r.get("decision") in ["reject","quarantine"]: decision = r["decision"]
            elif decision not in ["reject","quarantine"]: decision = r.get("decision", decision)
        required_terms = r.get("required_terms", [])
        has_required_terms = _all_required_terms_present(context, required_terms)
        if r.get("domain") == "work_vault" and required_terms:
            has_required_terms = has_required_terms and _work_vault_flags_true(context.get("content", {}), required_terms)
        if r.get("domain") in {"mark_allocation", "sovereign"} and required_terms:
            has_required_terms = has_required_terms and _required_keys_present(context.get("content", {}), required_terms)
        if has_required_terms is False and required_terms:
            matched.append(r["rule_id"]);viol.append("missing required terms: " + ",".join(required_terms))
            if r.get("missing_decision"): decision = r["missing_decision"]


    # allow negated boundary phrases
    if "does not claim achieved agi" in hay or "not empirical sota" in hay:
        if decision == "escalate": decision = "allow"
    sev = HARD_TERMS.get(decision, "medium")
    return make_decision(context, kernel, decision, sev, matched, viol, warn)


def evaluate_file(input_path, context_type="auto", kernel_path=None):
    from .policy_context import build_context
    if kernel_path is None:
        kernel_path = Path(__file__).resolve().parent.parent / "config" / "securerails_policy_kernel.json"
    kernel=load_kernel(kernel_path)
    rules=load_rules()
    return evaluate_context(build_context(input_path, context_type), kernel, rules)
