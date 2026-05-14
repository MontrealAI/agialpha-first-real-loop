import argparse, json, hashlib
from pathlib import Path
from .commercial_readiness import build_commercial_readiness
from .implementation_comparison import build_implementation_comparison
from .market_context import build_market_context
from .moat_assessment import build_moat_assessment
from .risk_boundary import build_risk_boundary
from .valuation_support_scorecard import build_scorecard

DISCLAIMER = "AGI ALPHA does not assert a valuation in this document. This dossier organizes implementation-side evidence that may support a valuation-comparable discussion. It is not investment advice, financial advice, a securities offering, a token-value claim, a guarantee of return, or a fair-market-value opinion."

def bfields():
    return {"claim_boundary":"valuation-support evidence only","token_boundary":"utility-only $AGIALPHA; no token value claim","regulated_boundary":"documentation_only","human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True}

def wj(p:Path, d): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(d, indent=2, sort_keys=True)+"\n")
def rj(p:Path): return json.loads(p.read_text()) if p.exists() else {}

def build(repo_root:Path, ascension_registry:Path, comparables:Path, out:Path, registry:Path=Path("valuation_support_registry")):
    comps=rj(comparables)
    entries=comps.get("comparables",[])
    market=[]
    for c in entries:
        row={"name":c.get("name","unavailable"),"reported_category_valuation_comparable":c.get("reported_category_valuation_comparable","not_reported"),"source":c.get("source","not_reported")}
        if row["reported_category_valuation_comparable"]=="not_reported":
            row["scenario_multiples"]="not_reported"
        else:
            row["scenario_multiples"]={str(m):m*float(c.get("revenue_proxy",1)) for m in [10,20,30,50]}
        market.append(row)
    manifest={"run_id":hashlib.sha256(str(out).encode()).hexdigest()[:12],"statement":DISCLAIMER,**bfields()}
    wj(out/"00_manifest.json",manifest)
    wj(out/"01_market_context.json", build_market_context(len(entries)))
    wj(out/"02_implementation_side_comparison.json", build_implementation_comparison(str(ascension_registry)))
    wj(out/"03_market_equivalence_sensitivity.json",{"rows":market or "not_reported",**bfields()})
    wj(out/"04_commercial_readiness.json", build_commercial_readiness())
    wj(out/"05_moat_assessment.json", build_moat_assessment())
    wj(out/"06_risk_boundary.json", build_risk_boundary())
    wj(out/"10_valuation_support_scorecard.json", build_scorecard())
    wj(out/"07_missing_evidence.json",{"missing":["audited external market data"],"status":"not_reported",**bfields()})
    (out/"08_valuation_support_memo.md").write_text(DISCLAIMER+"\n")
    (out/"09_not_an_investment_claim.md").write_text("Not an investment claim; scenario analysis only.\n")
    wj(out/"evidence-run-manifest.json",manifest)
    registry.mkdir(parents=True, exist_ok=True)
    wj(registry/"latest.json", manifest)
    wj(registry/"registry.json", {"records":[manifest]})

def validate(run:Path):
    req=["00_manifest.json","03_market_equivalence_sensitivity.json","09_not_an_investment_claim.md"]
    missing=[x for x in req if not (run/x).exists()]
    if missing: raise SystemExit(f"missing artifacts: {missing}")

def build_data(registry:Path, out:Path):
    out.mkdir(parents=True, exist_ok=True)
    latest=rj(registry/"latest.json")
    wj(out/"latest.json", latest or {"status":"unavailable",**bfields()})
    wj(out/"summary.json", {"statement":DISCLAIMER,**bfields()})
    mapping={"implementation_comparison":"02_implementation_side_comparison.json","market_equivalence_sensitivity":"03_market_equivalence_sensitivity.json","commercial_readiness":"04_commercial_readiness.json","moat_assessment":"05_moat_assessment.json","risk_boundary":"06_risk_boundary.json"}
    run=Path("valuation_support_registry/runs/test")
    for n,src in mapping.items():
        wj(out/f"{n}.json", rj(run/src) if (run/src).exists() else {"status":"not_reported",**bfields()})
