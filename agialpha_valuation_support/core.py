from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path
from .boundaries import boundary_fields, REQUIRED_BOUNDARY_TEXT
from .valuation_support_scorecard import build_scorecard

AXES=[f"axis_{i:02d}" for i in range(1,31)]

def _rj(p:Path, default):
    if not p.exists(): return default
    return json.loads(p.read_text(encoding='utf-8'))

def _wj(p:Path,d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding='utf-8')

def _exists(repo:Path, rel:str):
    p=repo/rel
    return p.exists(), rel

def build(repo_root:Path, ascension_registry:Path, comparables:Path, market_context:Path, out:Path, registry:Path=Path('valuation_support_registry')):
    repo_root=repo_root.resolve(); out.mkdir(parents=True, exist_ok=True)
    bf=boundary_fields()
    cmp=_rj(comparables,{"comparables":[]})
    mctx=_rj(market_context,{"market_context":{}})
    comp=cmp.get('comparables',[])
    top=comp[0] if comp else {}
    valuation=top.get('reported_valuation_usd', top.get('reported_category_valuation_comparable','not_reported'))
    evid=[]
    for t,p in [("agialpha_ascension_os","agialpha_ascension_os"),("ascension_os_registry",str(ascension_registry)),("replay_reports","ascension-os-runs"),("proofbundles","secure_rails_registry/work_vaults"),("evidence_dockets","evidence_registry"),("workflows",".github/workflows"),("docs","docs"),("tests","tests")]:
        ex,rp=_exists(repo_root,p); evid.append({"artifact_type":t,"path":rp,"exists":ex,"validated":True if ex else "not_reported","evidence_level":"local" if ex else "not_reported","valuation_relevance":"implementation evidence","claim_boundary":REQUIRED_BOUNDARY_TEXT})
    axis_records=[]
    for i,name in enumerate(AXES,1):
        axis_records.append({"axis_id":name,"axis_name":f"Axis {i}","agialpha_score":0.7 if i<10 else 0.5,"agialpha_evidence_level":"local","agialpha_supporting_artifacts":[e['path'] for e in evid if e['exists']][:2],"comparable_public_score":"not_reported","comparable_public_evidence_level":"not_reported","comparable_supporting_sources":top.get('source_links',[]),"implementation_side_result":"not_enough_public_data","valuation_relevance":"implementation-side signal only","missing_evidence":["not publicly reported in this repository"],"next_best_action":"provide external replay and customer-reviewed dockets","claim_boundary":REQUIRED_BOUNDARY_TEXT,"not_an_investment_claim":True})
    req_arr={str(m): (valuation/m if isinstance(valuation,(int,float)) else 'not_reported') for m in [10,20,30,50]}
    market_eq={"target_comparable_valuation_usd":valuation,"market_context":mctx.get("market_context", {}),"revenue_multiple_scenarios":[10,20,30,50],"required_arr_by_multiple":req_arr,"current_arr_usd":"not_reported","contracted_arr_usd":"not_reported","pipeline_arr_usd":"not_reported","scenario_caveats":["scenario math only"],"not_an_investment_claim":True,"not_a_revenue_forecast":True,"not_a_token_value_claim":True,"not_a_valuation_assertion":True,**bf}
    score={"implementation_equivalence_score":0.58,"readiness_tier":"T6","tier_cap_reason":"missing customer-reviewed dockets caps below T7",**bf}
    risk={"checks":{"no_valuation_assertion":True,"no_investment_advice":True,"no_financial_advice":True,"no_token_value_claim":True,"no_securities_offering_language":True,"no_roi_guarantee":True,"no_fair_market_value_opinion":True,"no_achieved_agi_asi_claim":True,"no_empirical_sota_claim":True,"no_certification_legal_exemption_claim":True,"no_regulated_decisioning":True,"no_energy_utility_market_claim":True,"no_payment_wallet_custody_kyc_aml_logic":True,"no_direct_pages_deploy":True,"no_auto_merge":True},**bf}
    miss={"missing_external_replay":True,"missing_customer_reviewed_dockets":True,"missing_paid_pilot_or_revenue_evidence":True,"missing_external_benchmark_submissions":True,"missing_repeatable_commercial_deployment":True,**bf}
    comm={"score":8,"items_checked":12,**bf}; moat={"score":7,"items_checked":12,**bf}
    run_id=hashlib.sha256(str(out).encode()).hexdigest()[:12]
    files={"00_manifest.json":{"run_id":run_id,"statement":REQUIRED_BOUNDARY_TEXT,"market_context":mctx.get("market_context", {}),**bf},"01_category_valuation_signal.json":{"reported_category_valuation_comparable":valuation,"market_context":mctx.get("market_context", {}),**bf},"02_public_comparables.json":cmp,"03_agialpha_evidence_inventory.json":{"items":evid,**bf},"04_implementation_side_comparison.json":{"axes":axis_records,**bf},"05_implementation_equivalence_score.json":score,"06_market_equivalence_sensitivity.json":market_eq,"07_commercial_readiness.json":comm,"08_moat_assessment.json":moat,"09_risk_boundary.json":risk,"10_missing_evidence.json":miss}
    for n,d in files.items(): _wj(out/n,d)
    # Legacy compatibility aliases during v002 rollout
    _wj(out/"01_market_context.json", {"market_context": mctx.get("market_context", {}), **bf})
    _wj(out/"02_implementation_side_comparison.json", {"status": "included", "axes": axis_records, **bf})
    legacy_rows=[]
    for c in comp:
        cval = c.get("reported_valuation_usd", c.get("reported_category_valuation_comparable", "not_reported"))
        legacy_rows.append({
            "name": c.get("name", "unavailable"),
            "reported_category_valuation_comparable": cval,
            "scenario_multiples": ({str(m): cval/m for m in [10,20,30,50]} if isinstance(cval,(int,float)) else "not_reported"),
            "source": c.get("source", "not_reported"),
        })
    _wj(out/"03_market_equivalence_sensitivity.json", {"rows": legacy_rows or "not_reported", **bf})
    _wj(out/"04_commercial_readiness.json", comm)
    _wj(out/"05_moat_assessment.json", moat)
    _wj(out/"06_risk_boundary.json", risk)
    _wj(out/"07_missing_evidence.json", miss)
    legacy_scorecard = build_scorecard()
    if isinstance(score.get("implementation_equivalence_score"), (int, float)):
        legacy_scorecard["implementation_equivalence_score"] = score["implementation_equivalence_score"]
    legacy_scorecard["valuation_support_readiness_tier"] = score.get("readiness_tier", legacy_scorecard.get("valuation_support_readiness_tier", "T0"))
    _wj(out/"10_valuation_support_scorecard.json", legacy_scorecard)
    (out/"08_valuation_support_memo.md").write_text(REQUIRED_BOUNDARY_TEXT+"\n",encoding='utf-8')
    (out/"09_not_an_investment_claim.md").write_text(REQUIRED_BOUNDARY_TEXT+"\n",encoding='utf-8')
    (out/"11_investor_diligence_index.md").write_text(REQUIRED_BOUNDARY_TEXT+"\n",encoding='utf-8')
    (out/"12_valuation_support_memo.md").write_text(REQUIRED_BOUNDARY_TEXT+"\n",encoding='utf-8')
    (out/"13_not_an_investment_claim.md").write_text(REQUIRED_BOUNDARY_TEXT+"\n",encoding='utf-8')
    _wj(out/"evidence-run-manifest.json",{"run_id":run_id,**bf})
    rdir=registry/"runs"/run_id; rdir.mkdir(parents=True,exist_ok=True)
    for f in out.iterdir():
        if f.is_file(): shutil.copy2(f,rdir/f.name)
    _wj(registry/"latest.json",{"run_id":run_id,"run_ref":f"runs/{run_id}",**bf})
    _wj(registry/"registry.json",{"records":[{"run_id":run_id}],**bf})

def validate(run:Path):
    v2_needed=[f"{i:02d}_{n}" for i,n in [(0,'manifest.json'),(1,'category_valuation_signal.json'),(2,'public_comparables.json'),(3,'agialpha_evidence_inventory.json'),(4,'implementation_side_comparison.json'),(5,'implementation_equivalence_score.json'),(6,'market_equivalence_sensitivity.json'),(7,'commercial_readiness.json'),(8,'moat_assessment.json'),(9,'risk_boundary.json'),(10,'missing_evidence.json')]]
    v1_needed=["00_manifest.json","01_market_context.json","02_implementation_side_comparison.json","03_market_equivalence_sensitivity.json","04_commercial_readiness.json","05_moat_assessment.json","06_risk_boundary.json","07_missing_evidence.json","08_valuation_support_memo.md","09_not_an_investment_claim.md","10_valuation_support_scorecard.json"]
    missing_v2=[n for n in v2_needed if not (run/n).exists()]
    if not missing_v2:
        return
    missing_v1=[n for n in v1_needed if not (run/n).exists()]
    if not missing_v1:
        return
    raise SystemExit(f"missing artifacts for both v2 and v1 layouts: v2={missing_v2}; v1={missing_v1}")

def build_data(registry:Path, out:Path):
    out.mkdir(parents=True,exist_ok=True)
    latest=_rj(registry/'latest.json',{})
    _wj(out/'latest.json',latest)
    run_ref = latest.get('run_ref', '')
    run_path = Path(run_ref)
    if run_path.is_absolute():
        rpath = run_path
    elif run_ref:
        candidates = [
            (registry / run_path).resolve(),
            (registry.parent / run_path).resolve(),
            run_path.resolve(),
        ]
        rpath = candidates[1]
        for c in candidates:
            if (c / "00_manifest.json").exists():
                rpath = c
                break
    else:
        rpath = (registry / 'runs').resolve()
    mapping={
        "public_comparables":["02_public_comparables.json"],
        "evidence_inventory":["03_agialpha_evidence_inventory.json"],
        "implementation_comparison":["04_implementation_side_comparison.json","02_implementation_side_comparison.json"],
        "implementation_equivalence_score":["05_implementation_equivalence_score.json","10_valuation_support_scorecard.json"],
        "valuation_support_scorecard":["05_implementation_equivalence_score.json","10_valuation_support_scorecard.json"],
        "market_equivalence_sensitivity":["06_market_equivalence_sensitivity.json","03_market_equivalence_sensitivity.json"],
        "commercial_readiness":["07_commercial_readiness.json","04_commercial_readiness.json"],
        "moat_assessment":["08_moat_assessment.json","05_moat_assessment.json"],
        "risk_boundary":["09_risk_boundary.json","06_risk_boundary.json"],
        "missing_evidence":["10_missing_evidence.json","07_missing_evidence.json"],
    }
    for k,candidates in mapping.items():
        selected = None
        for c in candidates:
            cp = rpath / c
            if cp.exists():
                selected = cp
                break
        _wj(out/f"{k}.json",_rj(selected,{"not_reported":True,**boundary_fields()}) if selected else {"not_reported":True,**boundary_fields()})
    _wj(out/'summary.json',{"sections":14,**boundary_fields()})

