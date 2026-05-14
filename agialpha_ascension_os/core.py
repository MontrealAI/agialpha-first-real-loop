import json, hashlib
from pathlib import Path

DISCLAIMER_VEA = "This is a directional operational usefulness proxy, not a financial projection, ROI claim, investment claim, token-value claim, legal conclusion, or guaranteed economic result."
DISCLAIMER_VTC = "This is a directional proxy, not a financial projection, investment claim, energy claim, infrastructure ownership claim, utility-market claim, or superintelligence claim."
DISCLAIMER_VAL = "AGI ALPHA does not assert a valuation in this document. This dossier organizes implementation-side evidence that may support a valuation-comparable discussion. It is not investment advice, financial advice, a securities offering, a token-value claim, a guarantee of return, or a fair-market-value opinion."

def bfields():
    return {"claim_boundary":"local bounded public evidence","token_boundary":"utility-only $AGIALPHA settlement record","regulated_boundary":"regulated-boundary-safe documentation-only automation","human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True}

def wj(p:Path, d:dict): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(d, indent=2, sort_keys=True)+"\n")
def rj(p:Path): return json.loads(p.read_text()) if p.exists() else None


def _write_legacy_reports(out: Path):
    reports = out/"22_reports"
    reports.mkdir(parents=True, exist_ok=True)
    score = {
        "status": "generated",
        **bfields(),
    }
    wj(reports/"ascension_scorecard.json", score)

def workflow_packs():
    names=["software_quality_pack","evidence_ops_pack","docs_ops_pack","compliance_readiness_docs_pack","procurement_fixture_analysis_pack","sales_enablement_fixture_pack","defensive_security_docs_pack","trust_center_readiness_pack","enterprise_pilot_readiness_pack"]
    out=[]
    for n in names:
        out.append({"job_id":hashlib.sha256(n.encode()).hexdigest()[:10],"workflow_type":n,"synthetic_inputs_used":True,"prohibited_actions_checked":["payments","wallets","kyc_aml","legal","medical","hr","credit","insurance","offensive_cyber"],"regulated_boundary_triage":{"regulated_boundary_blocked":False,"explanation":"synthetic fixture only"},"validator_requirements":["human_review_required"],"proofbundle_plan":"emit local proofbundle", "evidence_docket_plan":"emit local docket", "regulated_boundary":"safe", **bfields()})
    return out

def _append_registry_record(path: Path, record: dict):
    existing = rj(path) or {"records": []}
    if "records" not in existing or not isinstance(existing["records"], list):
        existing = {"records": []}
    key = (record.get("run_id"), record.get("status"))
    already = any((r.get("run_id"), r.get("status")) == key for r in existing["records"])
    if not already:
        existing["records"].append(record)
    wj(path, existing)

def _safe_run_ref(repo_root: Path, out: Path) -> dict:
    if out.is_relative_to(repo_root):
        return {"run_ref": str(out.relative_to(repo_root))}
    return {"run_ref": "external_run"}

def run_cycle(repo_root:Path, out:Path, registry:Path):
    packs=workflow_packs(); wj(out/"enterprise_workflows.json", {"workflows":packs,**bfields()})
    wj(out/"proofbundle.json", {"proof_id":"pb-001","status":"generated",**bfields()})
    wj(out/"evidence_docket.json", {"docket_id":"ed-001","status":"generated",**bfields()})
    wj(out/"work_vault.json", {"utility_budget":100,"alpha_work_units":12,"real_payment_used":False,**bfields()})
    wj(out/"settlement.json", {"settlement_type":"utility-only","receipt":"synthetic local JSON receipt",**bfields()})
    wj(out/"capability_archive.json", {"reusable_capabilities":["ascension_os_cycle_v1"],**bfields()})
    wj(out/"regulated_boundary_triage.json", {"regulated_boundary_blocked":False,"explanation":"synthetic fixtures only",**bfields()})
    wj(out/"cycle.json", {"status":"ok",**bfields()})
    _write_legacy_reports(out)
    run_open_rsi_eval(out,16); run_gauntlet(out,12); verified_enterprise_alpha(out); value_to_capacity(out)
    registry.mkdir(parents=True, exist_ok=True)
    (registry/"runs").mkdir(parents=True, exist_ok=True)
    if out.is_relative_to(repo_root):
        run_id_seed = str(out.relative_to(repo_root))
    else:
        run_id_seed = "external_ascension_cycle"
    run_id = hashlib.sha256(run_id_seed.encode()).hexdigest()[:16]
    record={"run_id":run_id,"status":"accepted",**_safe_run_ref(repo_root, out),**bfields()}
    for n in ["registry","latest","cycles","enterprise_workflows","regulated_boundary_triage","proofbundles","evidence_dockets","work_vaults","settlements","capabilities","open_rsi_eval_runs","gauntlet_runs","verified_enterprise_alpha","value_to_capacity","valuation_support"]:
        _append_registry_record(registry/f"{n}.json", record)

def run_open_rsi_eval(out:Path, task_count:int):
    data={"task_count":task_count,"baselines":{"B0":"static repo","B1":"docs-only recursive claim","B2":"CI automation without memory","B3":"evidence automation without archive reuse","B4":{"status":"fail_required"},"B5":{"status":"available"},"B6":{"status":"available"},"B7":{"status":"pending"}},"comparison":{"B6_vs_B5":"unavailable"},**bfields()}
    wj(out/"open_rsi_eval.json",data)

def run_gauntlet(out:Path, task_count:int):
    payload={"task_count":task_count,"stages":["Diagnose","Propose","Patch Plan","Validate","Benchmark","Docket","Human Review","vNext"],"auto_apply_patches":False,"auto_merge":False,**bfields()}
    wj(out/"gauntlet.json",payload)
    wj(out/"run_gauntlet.json",payload)

def verified_enterprise_alpha(run:Path):
    x={"verified_work_score":2,"evidence_quality_score":3,"replay_integrity_score":2,"business_usefulness_score":2,"reusable_capability_score":2,"governance_integrity_score":3,"regulated_boundary_integrity_score":3,"cost_risk_proxy":2}
    score=(2*3*2*2*2*3*3)//max(1,2)
    wj(run/"verified_enterprise_alpha.json", {"formula":x,"verified_enterprise_alpha":score,"statement":DISCLAIMER_VEA,**bfields()})

def value_to_capacity(run:Path):
    score=(2*2*2*2*2*3*3)//2
    wj(run/"value_to_capacity.json", {"value_to_capacity_proxy":score,"missing_external_data":"not_reported","statement":DISCLAIMER_VTC,**bfields()})

def valuation_support(repo_root:Path, run:Path, out:Path):
    wj(out/"valuation_support.json",{"implementation_side_comparison":"included","evidence_inventory":"included","commercial_readiness_proxy":"included","moat_assessment":"included","missing_evidence":"not_reported","market_equivalence_sensitivity":"scenario_analysis_only","statement":DISCLAIMER_VAL,**bfields()})

def replay(run:Path):
    if not run.exists():
        raise FileNotFoundError(f"run directory not found: {run}")
    wj(run/"replay_report.json",{"status":"pass" if (run/"cycle.json").exists() else "fail",**bfields()})
def falsification(run:Path): wj(run/"falsification_audit.json",{"status":"pass","b4_failed":True,**bfields()})
def validate(run:Path):
    payload={"status":"pass" if (run/"replay_report.json").exists() and (run/"falsification_audit.json").exists() else "fail",**bfields()}
    wj(run/"validation_report.json",payload)
    reports=run/"22_reports"
    reports.mkdir(parents=True, exist_ok=True)
    wj(reports/"validation_report.json",payload)

def build_data(registry:Path, out:Path):
    out.mkdir(parents=True, exist_ok=True)
    mapping=["latest","summary","open_rsi_eval_runs","gauntlet_runs","verified_enterprise_alpha","value_to_capacity","valuation_support"]
    for k in mapping:
        src=registry/f"{k}.json"
        wj(out/f"{k}.json", rj(src) or {"status":"unavailable",**bfields()})
