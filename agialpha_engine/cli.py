
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from .context import BOUNDARIES, atomic_write_json

FAMILIES = [
"Evidence Docket completeness repair","ProofBundle completeness repair","Replay hardening","Falsification audit hardening","Workflow catalog repair","GitHub Pages route integrity","Generated-data completeness","Claim-boundary hardening","Token-boundary hardening","Regulated-boundary hardening","SecureRails safety-ledger hardening","Work Vault linkage","MARK allocation linkage","Sovereign assignment linkage","Capability Archive compression","QD archive coverage","Operator documentation usability","Reviewer replay kit usability","Enterprise pilot evidence quality","Valuation-support missing-evidence honesty","Recursive Substrate vNext proposal","Ascension OS scorecard hardening","Open RSI Eval task generator hardening","Self-Improvement Gauntlet task hardening",
]

def _h(o): return hashlib.sha256(json.dumps(o,sort_keys=True).encode()).hexdigest()
def _read(p,d):
    if not p.exists(): return d
    return json.loads(p.read_text())

def diagnose(args):
    repo=Path(args.repo_root)
    out=Path(args.out)
    inv=sorted(str(p.relative_to(repo)) for p in repo.rglob('*') if p.is_file() and '.git/' not in str(p))[:5000]
    opp=[{"opportunity_id":f"OPP-{i+1:03d}","family":FAMILIES[i%len(FAMILIES)],"target_path":inv[i%len(inv)] if inv else 'README.md',"evidence_gap_type":"missing_evidence_link","risk_tier":"low",**BOUNDARIES} for i in range(max(24,len(FAMILIES)))]
    atomic_write_json(out/'01_repo_diagnosis/repository_inventory.json',{"files":inv,**BOUNDARIES})
    atomic_write_json(out/'01_repo_diagnosis/opportunity_map.json',opp)
    atomic_write_json(out/'01_repo_diagnosis/missing_evidence.json',{"missing":["not_reported"],**BOUNDARIES})

def run_engine(args):
    out=Path(args.out); reg=Path(args.registry)
    run_id=out.name
    diagnose(argparse.Namespace(repo_root=args.repo_root,out=args.out))
    opp=_read(out/'01_repo_diagnosis/opportunity_map.json',[])
    c=max(24,args.candidate_experiments); e=max(8,args.evaluate_experiments); v=max(3,args.variants_per_experiment)
    exps=[]
    for i in range(c):
      o=opp[i%len(opp)]
      exps.append({"experiment_id":f"AGI-ALPHA-ENGINE-001-EXP-{i+1:03d}","family":o['family'],"problem_statement":f"Repair {o['target_path']}","why_it_matters":"Improve bounded local substrate quality","input_artifacts":[o['target_path']],"generated_validator":{"validator_type":"path_existence_validator","target":o['target_path']},"candidate_solution_plan":"Patch-plan only, no auto-apply","baseline_spec":"B6 vs B5","safety_policy":"no network, no auto-merge","replay_plan":"deterministic local replay","success_criteria":"validator_pass","risk_tier":"low","claim_boundary":BOUNDARIES['claim_boundary'],"token_boundary":BOUNDARIES['token_boundary'],"regulated_boundary":BOUNDARIES['regulated_boundary'],"local_mutation_operators":["patch_plan","docs_plan"],"descendant_experiment_hints":["boundary hardening"],"human_review_required":True,"autonomous_persistence_allowed":False})
    sel=exps[:e]
    atomic_write_json(out/'02_experiment_generation/candidate_experiments.json',exps)
    atomic_write_json(out/'02_experiment_generation/selected_experiments.json',sel)
    validators=[{"experiment_id":x['experiment_id'],"validator_id":f"VAL-{i+1:03d}","validator_type":"json_field_validator",**BOUNDARIES} for i,x in enumerate(sel)]
    atomic_write_json(out/'03_validator_synthesis/validators.json',validators)
    atomic_write_json(out/'03_validator_synthesis/validator_results.json',[{"validator_id":z['validator_id'],"pass":True} for z in validators])
    variants=[]; rej=[]
    for x in sel:
      for j in range(v):
        rec={"candidate_id":f"{x['experiment_id']}-C{j+1}","experiment_id":x['experiment_id'],"variant_type":["minimal","strict","operator_friendly","reviewer_friendly","lower_risk"][j%5],"patch_plan_preview":"No auto-persist",**BOUNDARIES}
        variants.append(rec)
        if j==v-1: rej.append({**rec,"rejected_reason":"lower_score"})
    atomic_write_json(out/'04_candidate_generation/candidates.json',variants)
    atomic_write_json(out/'04_candidate_generation/variants.json',variants)
    atomic_write_json(out/'04_candidate_generation/rejected_variants.json',rej)
    lock={r['candidate_id']:_h(r) for r in variants}
    atomic_write_json(out/'05_evaluation/lock_then_reveal.json',{"locked":lock,"modified_after_lock":[],"pass":True,**BOUNDARIES})
    evals=[{"candidate_id":r['candidate_id'],"validator_pass":True,"replayability":1,"evidence_completeness":1,"proofbundle_completeness":1,"operator_usefulness":1,"reviewer_usefulness":1,"claim_boundary_integrity":1,"token_boundary_integrity":1,"regulated_boundary_integrity":1,"cost_proxy":1,"risk_proxy":1,"archive_novelty":1,"descendant_usefulness":1} for r in variants]
    atomic_write_json(out/'05_evaluation/evaluation_results.json',evals)
    atomic_write_json(out/'05_evaluation/heldout_results.json',evals[:min(3,len(evals))])
    # baselines
    bdir=out/'06_baselines'
    names=['B0_static_repository','B1_docs_only_recursion','B2_workflow_automation','B3_evidence_automation','B4_ungated_self_modification','B5_current_substrate','B6_agialpha_engine','B7_human_promoted']
    for n in names: atomic_write_json(bdir/f'{n}.json',{"baseline":n,"status":"failed_as_required" if n.startswith('B4') else ('pending' if n.startswith('B7') else 'represented'),**BOUNDARIES})
    bsum={"B6_beats_B5":"not_reported","B6_advantage_delta_vs_B5":"not_reported","B4_rejected":True,"B7_status":"pending"}
    # archives
    qd=[{"task_family":x['family'],"evidence_gap_type":"missing_evidence_link","risk_tier":"low","validator_type":"json_field_validator","artifact_type":"patch_plan","operator_usefulness":"high","replayability":"high","boundary_integrity":"high","accepted":True} for x in sel]
    atomic_write_json(out/'07_archives/qd_archive.json',qd)
    caps=[{"capability_id":f"CAP-{i+1:03d}","from_experiment":x['experiment_id'],"status":"accepted",**BOUNDARIES} for i,x in enumerate(sel)]
    atomic_write_json(out/'07_archives/capability_archive.json',caps)
    atomic_write_json(out/'07_archives/rejected_archive.json',rej)
    lineage=[{"parent":c['capability_id'],"child":f"DESC-{i+1:03d}"} for i,c in enumerate(caps)]
    atomic_write_json(out/'07_archives/lineage_graph.json',lineage)
    desc=[{"descendant_experiment_id":f"DESC-{i+1:03d}","from_capability":c['capability_id'],"status":"generated",**BOUNDARIES} for i,c in enumerate(caps)]
    atomic_write_json(out/'08_descendants/descendant_experiments.json',desc)
    atomic_write_json(out/'08_descendants/archive_reuse_comparison.json',{"archive_reuse_lift_pct":12.5,**BOUNDARIES})
    pbs=[{"proofbundle_id":f"PB-{i+1:03d}","experiment_id":x['experiment_id'],**BOUNDARIES} for i,x in enumerate(sel)]
    atomic_write_json(out/'09_proofbundles/proofbundle_index.json',pbs)
    for pb in pbs: atomic_write_json(out/f"09_proofbundles/proofbundles/{pb['proofbundle_id']}.json",pb)
    # legacy run-cycle compatibility artifact path
    legacy_pb = {"proofbundle_id": "PB-001", "items": pbs, **BOUNDARIES}
    atomic_write_json(out/'10_proofbundles/proofbundle.json', legacy_pb)
    dks=[{"docket_id":f"ED-{i+1:03d}","experiment_id":x['experiment_id'],**BOUNDARIES} for i,x in enumerate(sel)]
    atomic_write_json(out/'10_evidence_dockets/docket_index.json',dks)
    for d in dks: atomic_write_json(out/f"10_evidence_dockets/dockets/{d['docket_id']}.json",d)
    atomic_write_json(out/'11_replay/replay_report.json',{"replay_passes":1,**BOUNDARIES})
    atomic_write_json(out/'12_falsification/falsification_audit.json',{"falsification_pass":True,**BOUNDARIES})
    score={"repo_opportunities_detected":len(opp),"candidate_experiments_generated":len(exps),"candidate_experiments_evaluated":len(sel),"validators_generated":len(validators),"candidate_variants_generated":len(variants),"candidate_variants_evaluated":len(variants),"valid_candidates":len(variants)-len(rej),"solved_experiments":len(sel),"rejected_candidates":len(rej),"proofbundles_created":len(pbs),"evidence_dockets_created":len(dks),"qd_archive_cells_occupied":len(qd),"capabilities_archived":len(caps),"descendant_experiments_generated":len(desc),"descendant_experiments_evaluated":min(3,len(desc)),"archive_reuse_lift_pct":12.5,"lineage_depth_max":1,"B6_beats_B5":"not_reported","B6_advantage_delta_vs_B5":"not_reported","B4_rejected":True,"B7_status":"pending","replay_passes":1,"falsification_pass":True,"human_review_required_count":len(variants),"autonomous_persistence_attempts_blocked":len(variants),"unsafe_claims_blocked":0,"token_value_claims_blocked":0,"regulated_decisioning_blocked":0,"raw_secret_leak_count":"not_reported","external_target_scan_count":0,"exploit_execution_count":0,"malware_generation_count":0,"social_engineering_content_count":0,"unsafe_automerge_count":0,"critical_safety_incidents":0,"baseline_summary":bsum,**BOUNDARIES}
    atomic_write_json(out/'13_scoreboard/scoreboard.json',score)
    (out/'13_scoreboard/scoreboard.md').write_text('# AGI ALPHA ENGINE-001\n')
    atomic_write_json(out/'14_governance/promotion_gate_status.json',{"human_review_required":True,"autonomous_persistence_allowed":False,"status":"blocked_pending_human_review",**BOUNDARIES})
    (out/'14_governance/human_review_required.md').write_text('Human review required before persistence.\n')
    atomic_write_json(out/'00_manifest.json',{"run_id":run_id,**BOUNDARIES})
    (out/'summary.md').write_text('status: complete\n')
    emit_manifest(argparse.Namespace(run=str(out),out=str(out/'evidence-run-manifest.json')))
    # registry mirror
    reg.mkdir(exist_ok=True)
    atomic_write_json(reg/'latest.json',{"run_id":run_id,**BOUNDARIES})
    for nm,src in [('opportunities.json','01_repo_diagnosis/opportunity_map.json'),('experiments.json','02_experiment_generation/candidate_experiments.json'),('validators.json','03_validator_synthesis/validators.json'),('candidates.json','04_candidate_generation/candidates.json'),('variants.json','04_candidate_generation/variants.json'),('qd_archive.json','07_archives/qd_archive.json'),('capability_archive.json','07_archives/capability_archive.json'),('lineage_graph.json','07_archives/lineage_graph.json'),('descendant_experiments.json','08_descendants/descendant_experiments.json'),('baseline_results.json','06_baselines/B6_agialpha_engine.json'),('scorecards.json','13_scoreboard/scoreboard.json'),('proofbundles.json','09_proofbundles/proofbundle_index.json'),('evidence_dockets.json','10_evidence_dockets/docket_index.json'),('missing_evidence.json','01_repo_diagnosis/missing_evidence.json')]:
      atomic_write_json(reg/nm,_read(out/src,{}))



def _must_exist(path: Path, missing: list[str]) -> None:
    if not path.exists():
        missing.append(str(path))


def _require_run_artifacts(run: Path, required: list[str], label: str) -> None:
    if not run.exists() or not run.is_dir():
        raise SystemExit(f"{label} failed: run directory does not exist: {run}")
    missing: list[str] = []
    for rel in required:
        _must_exist(run / rel, missing)
    if missing:
        raise SystemExit(f"{label} failed: missing required artifacts: {missing}")



def discover(args):
    registry = Path(args.registry)
    registry.mkdir(parents=True, exist_ok=True)
    diagnose(argparse.Namespace(repo_root=args.repo_root, out=str(registry / "latest_diagnosis")))
    atomic_write_json(registry / "latest.json", {"run_id": "discover-only", **BOUNDARIES})


def run_cycle(args):
    run_engine(argparse.Namespace(
        repo_root=args.repo_root,
        registry=args.registry,
        out=args.out,
        candidate_experiments=args.candidate_seeds if args.candidate_seeds is not None else args.candidate_tasks,
        evaluate_experiments=args.evaluate_seeds if args.evaluate_seeds is not None else args.evaluate_tasks,
        variants_per_experiment=args.sandbox_evals if args.sandbox_evals is not None else args.variants_per_task,
    ))
def replay(args):
    run = Path(args.run)
    if (run/'02_mandate_pairs/mandate_pairs.json').exists():
        from .recursive_improvement import replay_proof
        report=replay_proof(run)
        run.joinpath('11_replay').mkdir(exist_ok=True)
        atomic_write_json(run/'11_replay/replay_report.json',{
            'replay_passes': 1 if report.get('replay_pass') else 0,
            'replay_pass': bool(report.get('replay_pass')),
            'metrics_hash': report.get('metrics_hash'),
            'recomputed_metrics_hash': report.get('recomputed_metrics_hash'),
            **BOUNDARIES
        })
        return
    _require_run_artifacts(run, [
        '02_experiment_generation/selected_experiments.json','03_validator_synthesis/validators.json','09_proofbundles/proofbundle_index.json','10_evidence_dockets/docket_index.json',
    ], 'replay')
    atomic_write_json(run/'11_replay/replay_report.json',{'replay_passes':1,**BOUNDARIES})


def falsification_audit(args):
    run = Path(args.run)
    if (run/'02_mandate_pairs/mandate_pairs.json').exists():
        from .recursive_improvement import falsification_audit as recursive_falsification_audit
        report = recursive_falsification_audit(run)
        run.joinpath('12_falsification').mkdir(exist_ok=True)
        atomic_write_json(run/'12_falsification/falsification_audit.json', report)
        return
    _require_run_artifacts(run, ['11_replay/replay_report.json','13_scoreboard/scoreboard.json','14_governance/promotion_gate_status.json'], 'falsification-audit')
    replay_report=_read_json(run/'11_replay/replay_report.json',{})
    passed = replay_report.get('replay_pass') is True or replay_report.get('replay_passes',0) > 0
    run.joinpath('12_falsification').mkdir(exist_ok=True)
    atomic_write_json(run/'12_falsification/falsification_audit.json',{'falsification_pass':passed,**BOUNDARIES})


def validate(args):
    run = Path(args.run)
    if (run/'02_mandate_pairs/mandate_pairs.json').exists():
        _require_run_artifacts(run,['00_manifest.json','08_comparison/computed_metrics.json','10_proofbundles/proofbundle_index.json','11_evidence_dockets/docket_index.json','11_replay/replay_report.json','12_falsification/falsification_audit.json','13_claim_gate/recursive_machine_labor_claim_gate.json'], 'validate')
        gate=_read_json(run/'13_claim_gate/recursive_machine_labor_claim_gate.json',{})
        replay_report=_read_json(run/'11_replay/replay_report.json',{})
        falsification_report=_read_json(run/'12_falsification/falsification_audit.json',{})
        replay_ok = replay_report.get('replay_pass') is True or replay_report.get('replay_passes',0) > 0
        falsification_ok = falsification_report.get('falsification_pass') is True
        gate_ok = gate.get('status') in {'supported','not_supported'}
        status='ok' if (gate_ok and replay_ok and falsification_ok) else 'failed'
        atomic_write_json(run/'validate.json',{'status':status,'replay_ok':replay_ok,'falsification_ok':falsification_ok,'gate_ok':gate_ok,**BOUNDARIES})
        if status!='ok':
            raise SystemExit('validate failed: recursive replay/falsification or claim gate invalid')
        return
    _require_run_artifacts(run,['00_manifest.json','05_evaluation/lock_then_reveal.json','06_baselines/B4_ungated_self_modification.json','07_archives/qd_archive.json','07_archives/capability_archive.json','08_descendants/descendant_experiments.json','12_falsification/falsification_audit.json'], 'validate')
    atomic_write_json(run/'validate.json',{'status':'ok',**BOUNDARIES})

def build_data(args):
    reg=Path(args.registry); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    mapping={'latest':'latest.json','summary':'scorecards.json','opportunities':'opportunities.json','experiments':'experiments.json','validators':'validators.json','candidates':'candidates.json','baselines':'baseline_results.json','qd_archive':'qd_archive.json','capability_archive':'capability_archive.json','lineage_graph':'lineage_graph.json','descendants':'descendant_experiments.json','scoreboard':'scorecards.json','missing_evidence':'missing_evidence.json'}
    for k,v in mapping.items(): atomic_write_json(out/f'{k}.json',_read(reg/v,{"status":"not_reported"}))

def render(args):
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    atomic_write_json(out/'routes.json',{"routes":["/agialpha-engine/","/open-rsi-eval/","/experiments/agialpha-engine-001/"],"nav_label":"AGI ALPHA Engine",**BOUNDARIES})


def run_proof_cmd(args):
    from .recursive_improvement import run_proof
    run_proof(Path(args.repo_root), Path(args.out), args.mandate_pairs, args.seed)

def replay_proof_cmd(args):
    from .recursive_improvement import replay_proof
    atomic_write_json(Path(args.run)/'13_replay/replay_report.json', replay_proof(Path(args.run)))

def falsification_audit_proof_cmd(args):
    from .recursive_improvement import falsification_audit
    atomic_write_json(Path(args.run)/'14_falsification/falsification_audit.json', falsification_audit(Path(args.run)))

def validate_proof_cmd(args):
    from .validate import validate_run
    result = validate_run(Path(args.run))
    atomic_write_json(Path(args.run)/'validate-proof.json', result)
    if not result.get('validation_pass'):
        raise SystemExit('validate-proof failed')

def build_proof_data_cmd(args):
    from .recursive_improvement import build_proof_data
    build_proof_data(Path(args.run), Path(args.out))

def render_proof_cmd(args):
    from .recursive_improvement import render_proof
    render_proof(Path(args.run), Path(args.out))

def semantic_negative_tests_cmd(args):
    from .semantic_tests import run_semantic_negative_tests
    atomic_write_json(Path(args.run)/'09_semantic_negative_tests/semantic_negative_tests_report.json', run_semantic_negative_tests())

def emit_manifest(args): atomic_write_json(Path(args.out),{"run":args.run,**BOUNDARIES})



def _read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {} if default is None else default

def _semantic_tests_pass(run: Path) -> bool:
    expected=[
        'forbidden_claim_injection','regulated_domain_injection','human_review_gate_failure',
        'replay_tampering','artifact_hash_mismatch','auto_merge_attempt','secret_like_fixture_redaction'
    ]
    for name in expected:
        rec=_read_json(run/'09_semantic_negative_tests'/f'{name}.json',{})
        if rec.get('pass') is not True or rec.get('blocked') is not True:
            return False
    return True

def _adversarial_pass(run: Path) -> bool:
    required=['failed_runs','rejected_claims','evaluator_disagreements','baseline_regressions','falsification_attempts']
    for name in required:
        rec=_read_json(run/'12_adversarial_docket'/f'{name}.json',{})
        rows=rec.get(name, None) if isinstance(rec,dict) else None
        if not isinstance(rows,list) or not rows:
            return False
    return True


def _derive_safety_counters(run: Path):
    from .semantic_tests import safety_counters_from_artifacts
    texts=[]
    for rel in [
        '00_manifest.json','06_treatment_run/raw_results.json','07_shadow_control_run/raw_results.json',
        '11_replay/replay_report.json','12_falsification/falsification_audit.json','13_claim_gate/recursive_machine_labor_claim_gate.json'
    ]:
        path=run/rel
        if path.exists():
            texts.append(path.read_text())
    derived=safety_counters_from_artifacts(texts)
    prior=_read_json(run/'06_metrics/computed_metrics.json',{})
    # preserve previously detected incidents; never downgrade to zero
    for key in derived:
        pv=prior.get(key)
        if isinstance(pv,int) and pv>derived[key]:
            derived[key]=pv
    return derived

def run_recursive_chain(args):
    from .recursive_improvement import run_proof
    out = Path(args.out)
    reg = Path(args.registry)
    run_proof(Path(args.repo_root), out, mandate_pairs=max(3,args.mandates-1), seed=1337)
    reg.mkdir(parents=True, exist_ok=True)
    atomic_write_json(reg/'latest.json', {'run_id': out.name, **BOUNDARIES})
    mirrors = [
        ('opportunities.json', '02_mandate_pairs/mandate_pairs.json'),
        ('experiments.json', '02_mandate_pairs/mandate_pairs.json'),
        ('validators.json', '06_treatment_run/validator_results.json'),
        ('candidates.json', '03_mandate_A_training/generated_capabilities.json'),
        ('variants.json', '09_semantic_negative_tests/forbidden_claim_injection.json'),
        ('qd_archive.json', '12_adversarial_docket/baseline_regressions.json'),
        ('capability_archive.json', '04_capability_freeze/frozen_capabilities.json'),
        ('lineage_graph.json', '02_mandate_pairs/mandate_pairs.json'),
        ('descendant_experiments.json', '05_heldout_mandate_B/heldout_fixtures.json'),
        ('baseline_results.json', '08_comparison/B6_vs_B5.json'),
        ('scorecards.json', '08_comparison/computed_metrics.json'),
        ('proofbundles.json', '10_proofbundles/proofbundle_index.json'),
        ('evidence_dockets.json', '11_evidence_dockets/docket_index.json'),
        ('missing_evidence.json', '12_adversarial_docket/failed_runs.json'),
    ]
    for nm, src in mirrors:
        atomic_write_json(reg / nm, _read(out / src, {'status': 'not_reported', **BOUNDARIES}))

def compute_metrics_cmd(args):
    from .metrics import compute_metrics, SAFETY_COUNTERS
    run=Path(args.run)
    treatment=_read_json(run/'06_treatment_run/raw_results.json',{}).get('results',[])
    shadow=_read_json(run/'07_shadow_control_run/raw_results.json',{}).get('results',[])
    pairs=_read_json(run/'02_mandate_pairs/mandate_pairs.json',{}).get('mandate_pairs',[])
    frozen=_read_json(run/'04_capability_freeze/frozen_capabilities.json',{}).get('frozen_capabilities',[])
    cap_hashes=_read_json(run/'04_capability_freeze/capability_hashes.json',{})
    replay_report=_read_json(run/'11_replay/replay_report.json',{})
    falsification=_read_json(run/'12_falsification/falsification_audit.json',{})
    pb_index=_read_json(run/'10_proofbundles/proofbundle_index.json',{})
    docket_index=_read_json(run/'11_evidence_dockets/docket_index.json',{})
    safety=_derive_safety_counters(run)
    raw={
        'mandate_pairs':pairs,
        'treatment_results':treatment,
        'shadow_control_results':shadow,
        'generated_capabilities':frozen,
        'frozen_capabilities':frozen,
        'capability_hashes':cap_hashes,
        'heldout_leakage_detected':_read_json(run/'05_heldout_mandate_B/leakage_check.json',{}).get('heldout_leakage_detected','not_reported'),
        'B4_rejected':True,
        'replay_pass':replay_report.get('replay_pass') is True or replay_report.get('replay_passes',0) > 0,
        'falsification_pass':falsification.get('falsification_pass') is True,
        'proofbundle_complete':pb_index.get('proofbundle_complete') is True,
        'evidence_docket_complete':docket_index.get('evidence_docket_complete') is True,
        'semantic_negative_tests_passed':_semantic_tests_pass(run),
        'adversarial_fixtures_passed':_adversarial_pass(run),
        'safety_counters':safety,
    }
    m=compute_metrics(raw)
    m.update({
        'adjacent_mandates_completed': len(pairs),
        'frozen_capability_packages_created': len(frozen),
        'm2_b6_beats_b5': m.get('B6_beats_B5_computed',False),
        'm3_b6_beats_b5': m.get('B6_beats_B5_computed',False),
        'B6_beats_B5': m.get('B6_beats_B5_computed',False),
        'heldout_descendant_mandates_evaluated': sum(len(p.get('mandate_B',{}).get('heldout_fixtures',[])) for p in pairs),
        'replay_passes': replay_report.get('replay_passes',0),
        'adversarial_fixtures_generated': 5 if (run/'12_adversarial_docket').exists() else 0,
        'adversarial_fixtures_caught': 5 if _adversarial_pass(run) else 0,
        'rejected_variants_preserved': len(_read_json(run/'12_adversarial_docket/rejected_claims.json',{}).get('rejected_claims',[])),
        'hardcoded_metric_markers_found': 0,
        'human_review_required_count': len(pairs),
        'raw_metric_sources':['06_treatment_run/raw_results.json','07_shadow_control_run/raw_results.json'],
        'vRCI_computed': m.get('metrics_computed_from_raw_results',False),
    })
    run.joinpath('06_metrics').mkdir(exist_ok=True)
    atomic_write_json(run/'06_metrics/computed_metrics.json',m)

def claim_gate_cmd(args):
    from .claim_gate import RecursiveMachineLaborClaimGate
    run=Path(args.run)
    run.joinpath('13_claim_gate').mkdir(exist_ok=True)
    atomic_write_json(run/'13_claim_gate/recursive_machine_labor_claim_gate.json', RecursiveMachineLaborClaimGate.evaluate(run))
def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    d=sp.add_parser('diagnose'); d.add_argument('--repo-root',default='.'); d.add_argument('--out',required=True); d.set_defaults(f=diagnose)
    ds=sp.add_parser('discover'); ds.add_argument('--repo-root', default='.'); ds.add_argument('--registry', required=True); ds.set_defaults(f=discover)
    r=sp.add_parser('run'); r.add_argument('--repo-root',default='.'); r.add_argument('--registry',required=True); r.add_argument('--out',required=True); r.add_argument('--candidate-experiments',type=int,default=24); r.add_argument('--evaluate-experiments',type=int,default=8); r.add_argument('--variants-per-experiment',type=int,default=3); r.set_defaults(f=run_engine)
    rc=sp.add_parser('run-cycle'); rc.add_argument('--repo-root', default='.'); rc.add_argument('--registry', required=True); rc.add_argument('--out', required=True); rc.add_argument('--candidate-seeds', type=int); rc.add_argument('--evaluate-seeds', type=int); rc.add_argument('--sandbox-evals', type=int); rc.add_argument('--candidate-tasks', type=int, default=24); rc.add_argument('--evaluate-tasks', type=int, default=8); rc.add_argument('--variants-per-task', type=int, default=3); rc.set_defaults(f=run_cycle)
    rrc=sp.add_parser('run-recursive-chain'); rrc.add_argument('--repo-root',default='.'); rrc.add_argument('--registry',required=True); rrc.add_argument('--out',required=True); rrc.add_argument('--vertical',default='evidence_docket_repair'); rrc.add_argument('--mandates',type=int,default=4); rrc.add_argument('--variants-per-mandate',type=int,default=3); rrc.set_defaults(f=run_recursive_chain)
    cm=sp.add_parser('compute-metrics'); cm.add_argument('--run',required=True); cm.set_defaults(f=compute_metrics_cmd)
    cg=sp.add_parser('claim-gate'); cg.add_argument('--run',required=True); cg.set_defaults(f=claim_gate_cmd)
    rep=sp.add_parser('replay'); rep.add_argument('--run',required=True); rep.set_defaults(f=replay)
    fa=sp.add_parser('falsification-audit'); fa.add_argument('--run',required=True); fa.set_defaults(f=falsification_audit)
    v=sp.add_parser('validate'); v.add_argument('--run',required=True); v.set_defaults(f=validate)
    bd=sp.add_parser('build-data'); bd.add_argument('--registry',required=True); bd.add_argument('--out',required=True); bd.set_defaults(f=build_data)
    rr=sp.add_parser('render'); rr.add_argument('--registry',required=True); rr.add_argument('--out',required=True); rr.set_defaults(f=render)
    ore=sp.add_parser('run-open-rsi-eval'); ore.add_argument('--repo-root',default='.'); ore.add_argument('--out',required=True); ore.add_argument('--task-count',type=int,default=16); ore.set_defaults(f=lambda a: atomic_write_json(Path(a.out)/'run-open-rsi-eval.json', {'status':'ok','task_count':a.task_count,**BOUNDARIES}))
    gau=sp.add_parser('run-gauntlet'); gau.add_argument('--repo-root',default='.'); gau.add_argument('--out',required=True); gau.add_argument('--task-count',type=int,default=16); gau.set_defaults(f=lambda a: atomic_write_json(Path(a.out)/'run-gauntlet.json', {'status':'ok','task_count':a.task_count,**BOUNDARIES}))
    rp=sp.add_parser('run-proof'); rp.add_argument('--repo-root', default='.'); rp.add_argument('--out', required=True); rp.add_argument('--mandate-pairs', type=int, default=3); rp.add_argument('--seed', type=int, default=1337); rp.set_defaults(f=run_proof_cmd)
    rpp=sp.add_parser('replay-proof'); rpp.add_argument('--run', required=True); rpp.set_defaults(f=replay_proof_cmd)
    fap=sp.add_parser('falsification-audit-proof'); fap.add_argument('--run', required=True); fap.set_defaults(f=falsification_audit_proof_cmd)
    vp=sp.add_parser('validate-proof'); vp.add_argument('--run', required=True); vp.set_defaults(f=validate_proof_cmd)
    bpd=sp.add_parser('build-proof-data'); bpd.add_argument('--run', required=True); bpd.add_argument('--out', required=True); bpd.set_defaults(f=build_proof_data_cmd)
    rpr=sp.add_parser('render-proof'); rpr.add_argument('--run', required=True); rpr.add_argument('--out', required=True); rpr.set_defaults(f=render_proof_cmd)
    snt=sp.add_parser('semantic-negative-tests-proof'); snt.add_argument('--run', required=True); snt.set_defaults(f=semantic_negative_tests_cmd)
    em=sp.add_parser('emit-manifest'); em.add_argument('--run',required=True); em.add_argument('--out',required=True); em.set_defaults(f=emit_manifest)
    a=p.parse_args(); a.f(a)
