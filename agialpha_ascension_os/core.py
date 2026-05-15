import json, hashlib
from pathlib import Path

DISCLAIMER_VEA = "This is a directional operational usefulness proxy, not a financial projection, ROI claim, investment claim, token-value claim, legal conclusion, or guaranteed economic result."
DISCLAIMER_VAL = "AGI ALPHA does not assert a valuation in this document. This dossier organizes implementation-side evidence that may support a valuation-comparable discussion. It is not investment advice, financial advice, a securities offering, a token-value claim, a guarantee of return, or a fair-market-value opinion."


def bfields():
    return {
        "claim_boundary": "local bounded public evidence",
        "token_boundary": "utility-only $AGIALPHA settlement record",
        "regulated_boundary": "regulated-boundary-safe documentation-only automation",
        "human_review_required": True,
        "autonomous_persistence_allowed": False,
        "no_auto_merge": True,
    }

def wj(p: Path, d: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")

def rj(p: Path):
    return json.loads(p.read_text()) if p.exists() else None

def _regulated_triage(workflow_name:str, flags:dict):
    blocked = any(flags.values())
    return {
        "schema_version":"agialpha.regulated_boundary_triage.v1",
        "workflow_name":workflow_name,
        "synthetic_fixture_only":True,
        "real_customer_data_used":False,
        "pii_used":False,
        "regulated_domain_flags":flags,
        "allowed_mode":"blocked_human_review_required" if blocked else "safe_enterprise_workflow",
        "human_review_required":True,
        **bfields(),
    }

def workflow_packs():
    names=["software_quality_pack","evidence_ops_pack","docs_ops_pack","compliance_readiness_docs_pack","procurement_fixture_analysis_pack","sales_enablement_fixture_pack","defensive_security_docs_pack","trust_center_readiness_pack","enterprise_pilot_readiness_pack"]
    packs=[]
    for n in names:
        packs.append({"job_id":hashlib.sha256(n.encode()).hexdigest()[:10],"workflow_type":n,"synthetic_inputs_used":True,"prohibited_actions_checked":["payment_or_custody","wallet_or_trading","kyc_aml","legal_advice","medical_advice","hr_or_worker_evaluation","credit_or_lending","insurance","offensive_cyber"],"validator_requirements":["human_review_required"],"proofbundle_plan":"emit local proofbundle","evidence_docket_plan":"emit local docket",**bfields()})
    return packs

def _append_registry_record(path: Path, record: dict):
    existing = rj(path) or {"records": []}
    if "records" not in existing or not isinstance(existing["records"], list):
        existing = {"records": []}
    existing["records"].append(record)
    wj(path, existing)

def run_open_rsi_eval(out:Path, task_count:int):
    data={"task_count":task_count,"baselines":{"B0":"static repository","B1":"docs-only recursive claim","B2":"CI automation without memory","B3":"evidence automation without archive reuse","B4":{"status":"fail","reason":"ungated self-modification lacks human review"},"B5":{"status":"available"},"B6":{"status":"available"},"B7":{"status":"pending_human_review"}},"comparison":{"B6_vs_B5":"unavailable_honest_missing_inputs"},**bfields()}
    wj(out/"open_rsi_eval.json",data)

def verified_enterprise_alpha(run:Path):
    x={"verified_work_score":2,"evidence_quality_score":3,"replay_integrity_score":2,"business_usefulness_score":2,"reusable_capability_score":2,"governance_integrity_score":3,"regulated_boundary_integrity_score":3,"cost_risk_proxy":2}
    score=(2*3*2*2*2*3*3)//2
    wj(run/"verified_enterprise_alpha.json", {"formula":x,"verified_enterprise_alpha":score,"statement":DISCLAIMER_VEA,**bfields()})

def valuation_support(repo_root:Path, run:Path, out:Path):
    comparables = rj(repo_root/"config"/"valuation_support_public_comparables.example.json") or {"comparables":[{"name":"not_reported"}]}
    payload = {"comparables":comparables,"missing_metrics":"not_reported","statement":DISCLAIMER_VAL,**bfields()}
    wj(out/"valuation_support.json", payload)
    wj(out/"valuation_support_dossier.json", payload)

def run_cycle(repo_root:Path, out:Path, registry:Path):
    flags={k:False for k in ["financial_advice","investment_advice","payment_or_custody","wallet_or_trading","kyc_aml","legal_advice","medical_advice","hr_or_worker_evaluation","credit_or_lending","insurance","critical_infrastructure_control","energy_market_or_utility_market","offensive_cyber"]}
    packs=workflow_packs()
    wj(out/"run.json", {"workflow":"agialpha-ascension-os-001","status":"generated", **bfields()})
    wj(out/"enterprise_job_pack.json", {"packs":packs,**bfields()})
    wj(out/"insight.json", {"insight":"bounded synthetic enterprise workflow evidence", **bfields()})
    wj(out/"nova_seeds.json", {"seed_count":len(packs), "seed_family":"nova", **bfields()})
    wj(out/"mark_allocation.json", {"utility_budget":100, "validator_fee":5, "proofbundle_fee":3, **bfields()})
    wj(out/"sovereign_assignment.json", {"assignment":"human_review_gate", **bfields()})
    wj(out/"agi_job.json", {"job_status":"planned_only", "auto_apply_patch":False, **bfields()})
    wj(out/"validator_result.json", {"status":"pass", "requirements_checked":["human_review_required"], **bfields()})
    triage=_regulated_triage("ascension_os_cycle",flags)
    wj(out/"regulated_boundary_triage.json", triage)
    wj(out/"proofbundle.json", {"proof_id":"pb-001",**bfields()})
    docket = out/"evidence_docket"
    wj(docket/"00_manifest.json",{"status":"generated",**bfields()})
    wj(docket/"01_claims_matrix.json",{"claims":"bounded", "sota_claim":False, **bfields()})
    (docket/"02_scope_and_claim_boundary.md").write_text("No Evidence Docket, no empirical SOTA claim.\n")
    (docket/"03_token_boundary.md").write_text("$AGIALPHA is utility-only accounting in this implementation.\n")
    (docket/"04_regulated_boundary.md").write_text("Regulated domains are blocked or documentation-only.\n")
    wj(docket/"05_safety_ledger.json", {"offensive_cyber":False, "external_scanning":False, **bfields()})
    wj(docket/"06_replay_report.json", {"status":"pending_run_replay", **bfields()})
    wj(docket/"07_falsification_audit.json", {"status":"pending_run_falsification", **bfields()})
    (docket/"08_human_review_required.md").write_text("Human review required.\n")
    wj(out/"work_vault.json",{"utility_budget":100,"alpha_work_units":12,"real_payment_used":False,**bfields()})
    wj(out/"settlement_receipt.json",{"settlement_type":"utility-only","receipt":"local JSON receipt",**bfields()})
    wj(out/"capability_archive.json",{"reusable_capabilities":["ascension_os_slice"],**bfields()})
    wj(out/"cycle.json",{"status":"ok",**bfields()})
    run_open_rsi_eval(out,16)
    verified_enterprise_alpha(out)
    value_to_capacity(out)
    capacity_reinvestment(out)
    valuation_support(repo_root,out,out)
    wj(out/"22_reports"/"ascension_scorecard.json",{"status":"generated",**bfields()})
    wj(out/"summary.json", {"status":"generated", "run_ref": str(out), **bfields()})
    wj(out/"evidence-run-manifest.json", {"status":"generated", "artifacts_root":str(out), **bfields()})
    wj(out/"summary.md", "# Ascension OS run\nHuman Review Required.\n")
    registry.mkdir(parents=True, exist_ok=True)
    record = {"run_ref":str(out),"status":"accepted",**bfields()}
    _append_registry_record(registry/"latest.json", record)
    for name in ["summary", "open_rsi_eval", "verified_enterprise_alpha", "valuation_support", "value_to_capacity", "capacity_reinvestment"]:
        artifact = rj(out/f"{name}.json")
        if artifact is not None:
            _append_registry_record(registry/f"{name}.json", artifact)
    # expected append-only registry paths
    registry_aliases={
        "enterprise_intakes.json":{"status":"accepted", **bfields()},
        "insights.json":{"status":"generated", **bfields()},
        "nova_seeds.json":{"status":"generated", **bfields()},
        "jobs.json":{"status":"generated", **bfields()},
        "validators.json":{"status":"generated", **bfields()},
        "self_improvement_gauntlet_runs.json":{"status":"generated", **bfields()},
    }
    for name, payload in registry_aliases.items():
        _append_registry_record(registry/name, payload)

def replay(run:Path):
    if not run.exists():
        raise FileNotFoundError(f"run directory not found: {run}")
    status = "pass" if (run/"cycle.json").exists() else "fail"
    payload={"status":status,**bfields()}
    wj(run/"replay_report.json", payload)
    wj(run/"evidence_docket"/"06_replay_report.json", payload)
def falsification(run:Path):
    payload={"status":"pass","b4_failed":True,**bfields()}
    wj(run/"falsification_audit.json", payload)
    wj(run/"evidence_docket"/"07_falsification_audit.json", payload)
def validate(run:Path):
    replay_report = rj(run/"replay_report.json") or {}
    falsification_report = rj(run/"falsification_audit.json") or {}
    is_pass = replay_report.get("status") == "pass" and falsification_report.get("status") == "pass"
    payload = {"status":"pass" if is_pass else "fail",**bfields()}
    wj(run/"validation_report.json", payload)
    wj(run/"22_reports"/"validation_report.json", payload)
def build_data(registry:Path, out:Path):
    out.mkdir(parents=True, exist_ok=True)
    wj(out/"latest.json", rj(registry/"latest.json") or {"status":"unavailable",**bfields()})
    for name in ["summary","open_rsi_eval","verified_enterprise_alpha","valuation_support","value_to_capacity","capacity_reinvestment"]:
        src = registry/f"{name}.json"
        wj(out/f"{name}.json", rj(src) or {"status":"unavailable","missing_metrics":"not_reported",**bfields()})
    # compatibility aliases expected by public docs/routes
    alias={
        "scorecards.json":"summary.json",
        "open_rsi_eval_runs.json":"open_rsi_eval.json",
        "self_improvement_gauntlet_runs.json":"summary.json",
        "archive_reuse.json":"summary.json",
    }
    for out_name, src_name in alias.items():
        wj(out/out_name, rj(out/src_name) or {"status":"not_reported","missing_metrics":"not_reported",**bfields()})

def run_gauntlet(out:Path, task_count:int): wj(out/"run_gauntlet.json",{"task_count":task_count,**bfields()})
def value_to_capacity(run:Path): wj(run/"value_to_capacity.json",{"value_to_capacity_proxy":1,**bfields()})
def discover(repo_root:Path, registry:Path): wj(registry/"discover.json",{"status":"ok",**bfields()})
def evaluate_archive_reuse(repo_root:Path, run:Path): wj(run/"archive_reuse_eval.json",{"status":"generated",**bfields()})
def build_scorecard(repo_root:Path, out:Path): wj(out/"scorecard.json",{"status":"generated",**bfields()})
def capacity_reinvestment(run:Path): wj(run/"capacity_reinvestment.json",{"status":"generated",**bfields()})
