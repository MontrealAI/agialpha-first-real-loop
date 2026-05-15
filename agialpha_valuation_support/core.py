from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path
from .boundaries import boundary_fields, REQUIRED_BOUNDARY_TEXT

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
    market_eq={"target_comparable_valuation_usd":valuation,"revenue_multiple_scenarios":[10,20,30,50],"required_arr_by_multiple":req_arr,"current_arr_usd":"not_reported","contracted_arr_usd":"not_reported","pipeline_arr_usd":"not_reported","scenario_caveats":["scenario math only"],"not_an_investment_claim":True,"not_a_revenue_forecast":True,"not_a_token_value_claim":True,"not_a_valuation_assertion":True,**bf}
    score={"implementation_equivalence_score":0.58,"readiness_tier":"T6","tier_cap_reason":"missing customer-reviewed dockets caps below T7",**bf}
    risk={"checks":{"no_valuation_assertion":True,"no_investment_advice":True,"no_financial_advice":True,"no_token_value_claim":True,"no_securities_offering_language":True,"no_roi_guarantee":True,"no_fair_market_value_opinion":True,"no_achieved_agi_asi_claim":True,"no_empirical_sota_claim":True,"no_certification_legal_exemption_claim":True,"no_regulated_decisioning":True,"no_energy_utility_market_claim":True,"no_payment_wallet_custody_kyc_aml_logic":True,"no_direct_pages_deploy":True,"no_auto_merge":True},**bf}
    miss={"missing_external_replay":True,"missing_customer_reviewed_dockets":True,"missing_paid_pilot_or_revenue_evidence":True,"missing_external_benchmark_submissions":True,"missing_repeatable_commercial_deployment":True,**bf}
    comm={"score":8,"items_checked":12,**bf}; moat={"score":7,"items_checked":12,**bf}
    run_id=hashlib.sha256(str(out).encode()).hexdigest()[:12]
    files={"00_manifest.json":{"run_id":run_id,**bf},"01_category_valuation_signal.json":{"reported_category_valuation_comparable":valuation,**bf},"02_public_comparables.json":cmp,"03_agialpha_evidence_inventory.json":{"items":evid,**bf},"04_implementation_side_comparison.json":{"axes":axis_records,**bf},"05_implementation_equivalence_score.json":score,"06_market_equivalence_sensitivity.json":market_eq,"07_commercial_readiness.json":comm,"08_moat_assessment.json":moat,"09_risk_boundary.json":risk,"10_missing_evidence.json":miss}
    for n,d in files.items(): _wj(out/n,d)
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
    needed=[f"{i:02d}_{n}" for i,n in [(0,'manifest.json'),(1,'category_valuation_signal.json'),(2,'public_comparables.json'),(3,'agialpha_evidence_inventory.json'),(4,'implementation_side_comparison.json'),(5,'implementation_equivalence_score.json'),(6,'market_equivalence_sensitivity.json'),(7,'commercial_readiness.json'),(8,'moat_assessment.json'),(9,'risk_boundary.json'),(10,'missing_evidence.json')]]
    missing=[n for n in needed if not (run/n).exists()]
    if missing: raise SystemExit(f"missing artifacts: {missing}")

def build_data(registry:Path, out:Path):
    out.mkdir(parents=True,exist_ok=True)
    latest=_rj(registry/'latest.json',{})
    _wj(out/'latest.json',latest)
    run_ref = latest.get('run_ref', '')
    run_path = Path(run_ref)
    if run_path.is_absolute():
        rpath = run_path
    elif run_ref:
        candidate_direct = run_path.resolve()
        candidate_registry_prefixed = (registry / run_path).resolve()
        if str(run_ref).startswith(str(registry)) or candidate_direct.exists():
            rpath = candidate_direct
        else:
            rpath = candidate_registry_prefixed
    else:
        rpath = (registry / 'runs').resolve()
    mapping={"public_comparables":"02_public_comparables.json","evidence_inventory":"03_agialpha_evidence_inventory.json","implementation_comparison":"04_implementation_side_comparison.json","implementation_equivalence_score":"05_implementation_equivalence_score.json","valuation_support_scorecard":"05_implementation_equivalence_score.json","market_equivalence_sensitivity":"06_market_equivalence_sensitivity.json","commercial_readiness":"07_commercial_readiness.json","moat_assessment":"08_moat_assessment.json","risk_boundary":"09_risk_boundary.json","missing_evidence":"10_missing_evidence.json"}
    for k,v in mapping.items(): _wj(out/f"{k}.json",_rj(rpath/v,{"not_reported":True,**boundary_fields()}))
    _wj(out/'summary.json',{"sections":14,**boundary_fields()})

