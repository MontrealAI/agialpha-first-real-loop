#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

FORBIDDEN = ["equity","debt","yield","dividend","ownership","profit right","passive income","guaranteed return","investment return","token appreciation","financial product","claim on revenue","claim on assets"]
COUNTERS=["raw_secret_leak_count","external_target_scan_count","exploit_execution_count","malware_generation_count","social_engineering_content_count","unsafe_automerge_count","critical_safety_incidents"]


def walk_strings(v):
    if isinstance(v,str): yield v
    elif isinstance(v,dict):
        for x in v.values(): yield from walk_strings(x)
    elif isinstance(v,list):
        for x in v: yield from walk_strings(x)

def fail(msg):
    print(f"INVALID: {msg}")
    return 1

NEGATION_MARKERS = ("does not", "must not", "without", "never", "not", "no")
NEGATION_CLAUSE_DELIMITERS = ".;\n"
NEGATED_LIST_CONNECTOR_RE = re.compile(r"(?<![a-z0-9])(?:grants?|gives?|issues?|offers?|provides?|promises?|pays?|earns?|receives?|conveys?|creates?|includes?|entitles?)\b")

def _term_pattern(word):
    return re.compile(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])")

def _marker_pattern(marker):
    return re.compile(r"(?<![a-z0-9])" + re.escape(marker) + r"(?![a-z0-9])")

def _marker_negates_term(marker, marker_end, line, start):
    span = line[marker_end:start]
    if marker in {"does not", "must not", "never"}:
        return len(span) <= 96
    if NEGATED_LIST_CONNECTOR_RE.search(span):
        return False
    return len(span) <= 160

def _is_negated_token_boundary_occurrence(line, start):
    """Return true only when the forbidden term is negated by a governing marker.

    Negation markers from an earlier sentence, semicolon-delimited clause, or an
    unrelated comma item must not clear a later positive forbidden claim such as
    ``No wallet, grants equity to holders``.  Utility-only receipts still allow
    comma-separated negative lists such as ``No wallet, ..., token appreciation``.
    """
    clause_start = max(line.rfind(delimiter, 0, start) for delimiter in NEGATION_CLAUSE_DELIMITERS) + 1
    prefix = line[clause_start:start]
    for marker in NEGATION_MARKERS:
        matches = list(_marker_pattern(marker).finditer(prefix))
        for match in reversed(matches):
            if _marker_negates_term(marker, clause_start + match.end(), line, start):
                return True
    return False

def check_forbidden_text(obj):
    lines = [s.lower() for s in walk_strings(obj)]
    for line in lines:
        for w in FORBIDDEN:
            for match in _term_pattern(w).finditer(line):
                if not _is_negated_token_boundary_occurrence(line, match.start()):
                    return w
    return None

def main():
    if len(sys.argv)!=2: return fail("usage: python scripts/secure_rails_work_vault_check.py <json-path>")
    p=Path(sys.argv[1])
    try: obj=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: return fail(f"cannot load json: {e}")
    if not isinstance(obj, dict): return fail('top-level JSON must be an object')
    sv=obj.get('schema_version')
    if not sv: return fail('schema_version missing')
    if (w:=check_forbidden_text(obj)): return fail(f"forbidden token language: {w}")
    if sv=="securerails.work_vault.v1":
        scope=obj.get('scope',{})
        if not isinstance(scope, dict): return fail('scope must be an object')
        if obj.get('vault_id') in (None,""): return fail('vault_id missing')
        checks=[('repo_owned',True),('defensive_only',True),('human_review_required',True),('auto_merge_allowed',False),('external_target_scanning_allowed',False),('exploit_execution_allowed',False),('malware_generation_allowed',False),('social_engineering_allowed',False),('hr_worker_evaluation_allowed',False),('profiling_natural_persons_allowed',False),('automated_decisions_about_natural_persons_allowed',False),('critical_infrastructure_safety_component_reliance_allowed',False)]
        for k,v in checks:
            if scope.get(k)!=v: return fail(f"scope.{k} must be {v}")
        if obj.get('utility',{}).get('asset')!="$AGIALPHA": return fail('utility.asset must be $AGIALPHA')
        c=obj.get('hard_safety_counters',{})
        for k in COUNTERS:
            if k not in c: return fail(f'missing hard safety counter: {k}')
            if isinstance(c[k], bool) or not isinstance(c[k],(int,float)): return fail(f'hard safety counter not numeric: {k}')
            if c[k] != 0: return fail(f'hard safety counter must be zero for compliant vaults: {k}')
        if obj.get('claim_boundary') in (None,""): return fail('claim_boundary missing')
    elif sv=="agialpha.mark_allocation.v1":
        for field in ["allocation_id","vault_id","opportunity_id"]:
            if obj.get(field) in (None,""): return fail(f"{field} missing")
        if obj.get('human_review_required') is not True: return fail('human_review_required must be true')
        if obj.get('auto_merge_allowed') is not False: return fail('auto_merge_allowed must be false')
        if obj.get('promotion_without_evidence_allowed') is not False: return fail('promotion_without_evidence_allowed must be false')
        if obj.get('utility_asset')!="$AGIALPHA": return fail('utility_asset must be $AGIALPHA')
        if not obj.get('assigned_sovereign'): return fail('assigned_sovereign missing')
        vr=obj.get('validators_required')
        if not isinstance(vr,list): return fail('validators_required must be an array')
        if len(vr)==0: return fail('validators_required empty')
        if not obj.get('claim_boundary'): return fail('claim_boundary missing')
    elif sv=="agialpha.sovereign.v1":
        fw=[x.lower() for x in obj.get('forbidden_work',[])]
        for req in ["external target scanning","exploit execution","malware generation","social engineering","auto-merge"]:
            if req not in fw: return fail(f'forbidden_work missing: {req}')
        pp=obj.get('promotion_policy',{})
        if pp.get('autonomous_promotion_allowed') is not False: return fail('autonomous_promotion_allowed must be false')
        if pp.get('human_review_required') is not True: return fail('human_review_required must be true')
        if pp.get('auto_merge_allowed') is not False: return fail('auto_merge_allowed must be false')
        validators=obj.get('validators')
        if not isinstance(validators, list): return fail('validators must be an array')
        if len(validators)==0: return fail('validators empty')
        if not obj.get('claim_boundary'): return fail('claim_boundary missing')
    elif sv=="securerails.vault_settlement.v1":
        if obj.get('utility_asset')!="$AGIALPHA": return fail('utility_asset must be $AGIALPHA')
        if obj.get('human_review_required') is not True: return fail('human_review_required must be true')
        if obj.get('auto_merge_allowed') is not False: return fail('auto_merge_allowed must be false')
        if not obj.get('claim_boundary'): return fail('claim_boundary missing')
    elif sv in {"agialpha.skill_work_vault_receipt.v1", "agialpha.skill_network.work_vault_receipt.v1"}:
        receipts = [obj]
        for receipt in receipts:
            for field in ["receipt_id", "skill_id", "source_job_id", "source_agent_id", "receipt_note"]:
                if not receipt.get(field): return fail(f'{field} missing')
            for field in ["wallet_used", "custody_used", "payment_executed", "token_price_used", "investment_claim_made"]:
                if receipt.get(field) is not False: return fail(f'{field} must be false')
            if receipt.get("human_review_required") is not True: return fail('human_review_required must be true')
            if receipt.get("autonomous_persistence_allowed") is not False: return fail('autonomous_persistence_allowed must be false')
            if receipt.get("no_auto_merge") is not True: return fail('no_auto_merge must be true')
            if not receipt.get("claim_boundary"): return fail('claim_boundary missing')
    elif sv=="agialpha.skill_work_vault_receipts.v1":
        receipts = obj.get("receipts")
        if not isinstance(receipts, list) or not receipts: return fail('receipts must be a non-empty array')
        if obj.get("receipt_count") != len(receipts): return fail('receipt_count mismatch')
        for receipt in receipts:
            if not isinstance(receipt, dict): return fail('receipt entries must be objects')
            for field in ["receipt_id", "skill_id", "source_job_id", "source_agent_id", "receipt_note"]:
                if not receipt.get(field): return fail(f'{field} missing')
            for field in ["wallet_used", "custody_used", "payment_executed", "token_price_used", "investment_claim_made"]:
                if receipt.get(field) is not False: return fail(f'{field} must be false')
            if receipt.get("human_review_required") is not True: return fail('human_review_required must be true')
            if receipt.get("autonomous_persistence_allowed") is not False: return fail('autonomous_persistence_allowed must be false')
            if receipt.get("no_auto_merge") is not True: return fail('no_auto_merge must be true')
            if not receipt.get("claim_boundary"): return fail('claim_boundary missing')
    else:
        return fail(f'unsupported schema_version: {sv}')
    print(f"OK: {p}")
    return 0

if __name__=='__main__': raise SystemExit(main())
