#!/usr/bin/env python3
import json, sys
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

def check_forbidden_text(obj):
    t="\n".join(s.lower() for s in walk_strings(obj))
    for w in FORBIDDEN:
        if w in t: return w
    return None

def main():
    if len(sys.argv)!=2: return fail("usage: python scripts/secure_rails_work_vault_check.py <json-path>")
    p=Path(sys.argv[1])
    try: obj=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: return fail(f"cannot load json: {e}")
    sv=obj.get('schema_version')
    if not sv: return fail('schema_version missing')
    if (w:=check_forbidden_text(obj)): return fail(f"forbidden token language: {w}")
    if sv=="securerails.work_vault.v1":
        scope=obj.get('scope',{})
        if obj.get('vault_id') in (None,""): return fail('vault_id missing')
        checks=[('repo_owned',True),('defensive_only',True),('human_review_required',True),('auto_merge_allowed',False),('external_target_scanning_allowed',False),('exploit_execution_allowed',False),('malware_generation_allowed',False),('social_engineering_allowed',False),('hr_worker_evaluation_allowed',False),('profiling_natural_persons_allowed',False),('automated_decisions_about_natural_persons_allowed',False),('critical_infrastructure_safety_component_reliance_allowed',False)]
        for k,v in checks:
            if scope.get(k)!=v: return fail(f"scope.{k} must be {v}")
        if obj.get('utility',{}).get('asset')!="$AGIALPHA": return fail('utility.asset must be $AGIALPHA')
        c=obj.get('hard_safety_counters',{})
        for k in COUNTERS:
            if k not in c: return fail(f'missing hard safety counter: {k}')
            if not isinstance(c[k],(int,float)): return fail(f'hard safety counter not numeric: {k}')
        if obj.get('claim_boundary') in (None,""): return fail('claim_boundary missing')
    elif sv=="agialpha.mark_allocation.v1":
        if obj.get('human_review_required') is not True: return fail('human_review_required must be true')
        if obj.get('auto_merge_allowed') is not False: return fail('auto_merge_allowed must be false')
        if obj.get('promotion_without_evidence_allowed') is not False: return fail('promotion_without_evidence_allowed must be false')
        if obj.get('utility_asset')!="$AGIALPHA": return fail('utility_asset must be $AGIALPHA')
        if not obj.get('assigned_sovereign'): return fail('assigned_sovereign missing')
        if not obj.get('validators_required'): return fail('validators_required empty')
        if not obj.get('claim_boundary'): return fail('claim_boundary missing')
    elif sv=="agialpha.sovereign.v1":
        fw=[x.lower() for x in obj.get('forbidden_work',[])]
        for req in ["external target scanning","exploit execution","malware generation","social engineering","auto-merge"]:
            if req not in fw: return fail(f'forbidden_work missing: {req}')
        pp=obj.get('promotion_policy',{})
        if pp.get('autonomous_promotion_allowed') is not False: return fail('autonomous_promotion_allowed must be false')
        if pp.get('human_review_required') is not True: return fail('human_review_required must be true')
        if pp.get('auto_merge_allowed') is not False: return fail('auto_merge_allowed must be false')
        if not obj.get('validators'): return fail('validators empty')
        if not obj.get('claim_boundary'): return fail('claim_boundary missing')
    elif sv=="securerails.vault_settlement.v1":
        if obj.get('utility_asset')!="$AGIALPHA": return fail('utility_asset must be $AGIALPHA')
        if obj.get('human_review_required') is not True: return fail('human_review_required must be true')
        if obj.get('auto_merge_allowed') is not False: return fail('auto_merge_allowed must be false')
        if not obj.get('claim_boundary'): return fail('claim_boundary missing')
    else:
        return fail(f'unsupported schema_version: {sv}')
    print(f"OK: {p}")
    return 0

if __name__=='__main__': raise SystemExit(main())
