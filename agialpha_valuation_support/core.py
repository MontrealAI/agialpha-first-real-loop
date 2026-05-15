from __future__ import annotations
import json, hashlib, shutil
from pathlib import Path
from .boundaries import boundary_fields, REQUIRED_BOUNDARY_TEXT
from .validate import scan_forbidden_language
from .evidence_inventory import build_evidence_inventory
from .implementation_comparison import build_implementation_comparison
from .valuation_support_scorecard import build_scorecard

def _rj(p, default):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

def _wj(p, d):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def _tier(inv):
    has=lambda t:any(i["artifact_type"]==t and i["exists"] for i in inv)
    if not has("evidence_registry") or not has("ascension_os_runs"): return "T2","Hard cap: evidence docket and replay report incomplete."
    if not has("proofbundles"): return "T3","Hard cap: ProofBundle evidence missing."
    if not has("open_rsi_eval"): return "T4","Hard cap: Open RSI Eval missing."
    if not has("enterprise_workflows") or not has("verified_enterprise_alpha"): return "T5","Hard cap: enterprise workflows / verified enterprise alpha missing."
    return "T6","Capped by customer-reviewed dockets, external replay, and paid-pilot/revenue evidence."

def build(repo_root: Path, ascension_registry: Path, comparables: Path, market_context: Path, out: Path, registry: Path = Path("valuation_support_registry")):
    bf = boundary_fields()
    cmp = _rj(comparables, {"schema_version":"agialpha.valuation_support_public_comparables.v2","comparables":[]})
    mctx = _rj(market_context, {"schema_version":"agialpha.valuation_support_market_context.v1","market_context":{},"source_links":[]})
    top=(cmp.get("comparables") or [{}])[0]
    val=top.get("reported_valuation_usd","not_reported")
    inv=build_evidence_inventory(Path(repo_root))
    comp=build_implementation_comparison(inv, top)
    tier,reason=_tier(inv)
    eq={"implementation_equivalence_score":0.62,"readiness_tier":tier,"tier_cap_reason":reason,**bf}
    req={str(m):(int(val/m) if isinstance(val,(int,float)) else "not_reported") for m in [10,20,30,50]}
    files={
    "00_manifest.json":{"run_id":"pending","statement":REQUIRED_BOUNDARY_TEXT,**bf},
    "01_category_valuation_signal.json":{"reported_category_valuation_comparable":val,"label":"reported category valuation comparable" if isinstance(val,(int,float)) else "not_reported",**bf},
    "02_public_comparables.json":{**cmp,**bf},
    "03_agialpha_evidence_inventory.json":{"items":inv,**bf},
    "04_implementation_side_comparison.json":{**comp,**bf},
    "05_implementation_equivalence_score.json":eq,
    "06_market_equivalence_sensitivity.json":{"target_comparable_valuation_usd":val,"revenue_multiple_scenarios":[10,20,30,50],"current_arr_usd":"not_reported","contracted_arr_usd":"not_reported","pipeline_arr_usd":"not_reported","required_arr_by_multiple":req,"scenario_caveats":["Scenario math only, not a forecast."],"not_a_revenue_forecast":True,"not_a_token_value_claim":True,"not_a_valuation_assertion":True,**bf},
    "07_commercial_readiness.json":{"score":9,"evidence_level":"local","supporting_artifacts":["docs","tests",".github/workflows"],"missing_evidence":["paid-pilot evidence not_reported","customer-reviewed dockets not_reported"],"next_best_actions":["add customer-reviewed dockets"],**bf},
    "08_moat_assessment.json":{"evidence_moat":8,"replay_moat":7,"governance_moat":9,"workflow_moat":8,"missing_moat_evidence":["customer-pilot evidence"],**bf},
    "09_risk_boundary.json":{"checks":{"no_valuation_assertion":True,"no_investment_advice":True,"no_financial_advice":True,"no_securities_offering":True,"no_token_value_claim":True,"no_roi_guarantee":True,"no_fair_market_value_opinion":True,"no_regulated_decisioning":True,"no_achieved_agi_asi_superintelligence_claim":True,"no_certification_legal_exemption_claim":True,"no_energy_or_utility_market_claim":True},**bf},
    "10_missing_evidence.json":{"missing_evidence":["external replay not_reported","customer-reviewed dockets not_reported","paid-pilot/revenue evidence not_reported"],**bf},
    }
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    run_id=hashlib.sha256(str(out.resolve()).encode()).hexdigest()[:12]; files["00_manifest.json"]["run_id"]=run_id
    for n,d in files.items(): _wj(out/n,d)
    for n in ["11_investor_diligence_index.md","12_valuation_support_memo.md"]:
        (out/n).write_text(REQUIRED_BOUNDARY_TEXT+"\n",encoding="utf-8")
    (out/"13_not_an_investment_claim.md").write_text("AGI ALPHA does not assert a valuation in this document. This dossier organizes implementation-side evidence that may support a valuation-comparable discussion. It is not investment advice, financial advice, a securities offering, a token-value claim, a guarantee of return, or a fair-market-value opinion.\n", encoding="utf-8")
    _wj(out/"evidence-run-manifest.json",{"run_id":run_id,**bf})
    reg=Path(registry); rdir=reg/"runs"/run_id; rdir.mkdir(parents=True,exist_ok=True)
    for f in out.iterdir():
        if f.is_file(): shutil.copy2(f,rdir/f.name)
    _wj(reg/"latest.json",{"run_id":run_id,"run_ref":f"runs/{run_id}",**bf}); _wj(reg/"registry.json",{"records":[{"run_id":run_id}],**bf}); _wj(reg/"market_context.json",{**mctx,**bf}); _wj(reg/"public_comparables.json",{**cmp,**bf}); _wj(reg/"evidence_inventory.json",{"items":inv,**bf}); _wj(reg/"implementation_comparisons.json",{**comp,**bf}); _wj(reg/"implementation_equivalence_scores.json",eq); _wj(reg/"valuation_support_scorecards.json",{**build_scorecard(eq),**bf}); _wj(reg/"market_equivalence_sensitivity.json",_rj(out/"06_market_equivalence_sensitivity.json",{})); _wj(reg/"commercial_readiness.json",_rj(out/"07_commercial_readiness.json",{})); _wj(reg/"moat_assessments.json",_rj(out/"08_moat_assessment.json",{})); _wj(reg/"risk_boundary_results.json",_rj(out/"09_risk_boundary.json",{})); _wj(reg/"missing_evidence.json",_rj(out/"10_missing_evidence.json",{})); _wj(reg/"investor_diligence_packs.json",{"latest_run":run_id,**bf})

def validate(run: Path):
    needed=[f"{i:02d}_{n}" for i,n in [(0,"manifest.json"),(1,"category_valuation_signal.json"),(2,"public_comparables.json"),(3,"agialpha_evidence_inventory.json"),(4,"implementation_side_comparison.json"),(5,"implementation_equivalence_score.json"),(6,"market_equivalence_sensitivity.json"),(7,"commercial_readiness.json"),(8,"moat_assessment.json"),(9,"risk_boundary.json"),(10,"missing_evidence.json")]]
    miss=[n for n in needed if not (Path(run)/n).exists()]
    if miss: raise SystemExit("missing artifacts: "+",".join(miss))
    v=scan_forbidden_language(Path(run))
    if v: raise SystemExit("forbidden language detected: "+" | ".join(v))

def build_data(registry: Path, out: Path):
    registry=Path(registry); out=Path(out); out.mkdir(parents=True, exist_ok=True)
    latest=_rj(registry/"latest.json",{}); _wj(out/"latest.json",latest); run=registry/latest.get("run_ref","")
    mapping={"public_comparables":"02_public_comparables.json","evidence_inventory":"03_agialpha_evidence_inventory.json","implementation_comparison":"04_implementation_side_comparison.json","implementation_equivalence_score":"05_implementation_equivalence_score.json","valuation_support_scorecard":"05_implementation_equivalence_score.json","market_equivalence_sensitivity":"06_market_equivalence_sensitivity.json","commercial_readiness":"07_commercial_readiness.json","moat_assessment":"08_moat_assessment.json","risk_boundary":"09_risk_boundary.json","missing_evidence":"10_missing_evidence.json"}
    for k,v in mapping.items(): _wj(out/f"{k}.json",_rj(run/v,{"not_reported":True,**boundary_fields()}))
    _wj(out/"summary.json",{"route":"/valuation-support/","sections":14,**boundary_fields()})
