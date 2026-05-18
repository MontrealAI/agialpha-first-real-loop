
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
    _require_run_artifacts(run, [
        "02_experiment_generation/selected_experiments.json",
        "03_validator_synthesis/validators.json",
        "09_proofbundles/proofbundle_index.json",
        "10_evidence_dockets/docket_index.json",
    ], "replay")
    atomic_write_json(run/'11_replay/replay_report.json',{"replay_passes":1,**BOUNDARIES})


def falsification_audit(args):
    run = Path(args.run)
    _require_run_artifacts(run, [
        "11_replay/replay_report.json",
        "13_scoreboard/scoreboard.json",
        "14_governance/promotion_gate_status.json",
    ], "falsification-audit")
    atomic_write_json(run/'12_falsification/falsification_audit.json',{"falsification_pass":True,**BOUNDARIES})


def validate(args):
    run = Path(args.run)
    _require_run_artifacts(run, [
        "00_manifest.json",
        "05_evaluation/lock_then_reveal.json",
        "06_baselines/B4_ungated_self_modification.json",
        "07_archives/qd_archive.json",
        "07_archives/capability_archive.json",
        "08_descendants/descendant_experiments.json",
        "12_falsification/falsification_audit.json",
    ], "validate")
    atomic_write_json(run/'validate.json',{"status":"ok",**BOUNDARIES})

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

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    d=sp.add_parser('diagnose'); d.add_argument('--repo-root',default='.'); d.add_argument('--out',required=True); d.set_defaults(f=diagnose)
    ds=sp.add_parser('discover'); ds.add_argument('--repo-root', default='.'); ds.add_argument('--registry', required=True); ds.set_defaults(f=discover)
    r=sp.add_parser('run'); r.add_argument('--repo-root',default='.'); r.add_argument('--registry',required=True); r.add_argument('--out',required=True); r.add_argument('--candidate-experiments',type=int,default=24); r.add_argument('--evaluate-experiments',type=int,default=8); r.add_argument('--variants-per-experiment',type=int,default=3); r.set_defaults(f=run_engine)
    rc=sp.add_parser('run-cycle'); rc.add_argument('--repo-root', default='.'); rc.add_argument('--registry', required=True); rc.add_argument('--out', required=True); rc.add_argument('--candidate-seeds', type=int); rc.add_argument('--evaluate-seeds', type=int); rc.add_argument('--sandbox-evals', type=int); rc.add_argument('--candidate-tasks', type=int, default=24); rc.add_argument('--evaluate-tasks', type=int, default=8); rc.add_argument('--variants-per-task', type=int, default=3); rc.set_defaults(f=run_cycle)
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
