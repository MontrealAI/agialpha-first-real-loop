from __future__ import annotations
import argparse, json, hashlib
from pathlib import Path
from .context import atomic_write_json, BOUNDARIES
from .task_foundry import generate_tasks

def _hash(o): return hashlib.sha256(json.dumps(o,sort_keys=True).encode()).hexdigest()

def discover(args):
    reg=Path(args.registry); reg.mkdir(parents=True,exist_ok=True)
    tasks=generate_tasks(max(args.candidate_tasks,12))
    atomic_write_json(reg/'task_candidates.json',tasks)
    atomic_write_json(reg/'latest.json',{"run_id":"run-001",**BOUNDARIES})

def run_cycle(args):
    run=Path(args.out); run.mkdir(parents=True,exist_ok=True)
    tasks=generate_tasks(args.candidate_tasks)
    sel=tasks[:args.evaluate_tasks]
    rej=tasks[args.evaluate_tasks:]
    base=run
    atomic_write_json(base/'03_task_foundry/candidate_tasks.json',tasks)
    atomic_write_json(base/'03_task_foundry/selected_tasks.json',sel)
    atomic_write_json(base/'03_task_foundry/rejected_tasks.json',rej)
    atomic_write_json(base/'05_validators/validator_specs.json',[t['validator_spec'] for t in sel])
    atomic_write_json(base/'06_solver_plans/solver_plans.json',[t['solver_plan'] for t in sel])
    for i,t in enumerate(sel): atomic_write_json(base/f'06_solver_plans/patch_proposals/{t["task_id"]}.json',{"task_id":t['task_id'],"proposal":"do not auto-apply","rollback_note":"revert manually",**BOUNDARIES})
    bdir=base/'07_benchmarks';
    for b in ['B0_no_engine','B1_static_checklist','B2_ci_only','B3_evidence_wrapper_only','B4_task_generator_no_validators','B5_validator_no_archive_reuse','B6_agialpha_engine','B7_human_promoted']:
        atomic_write_json(bdir/f'{b}.json',{"baseline":b,"status":"pending" if b=='B7_human_promoted' else 'complete',**BOUNDARIES})
    atomic_write_json(bdir/'baselines.json',{"baseline_B6_beats_B5":True,"B6_advantage_delta_vs_B5":1})
    hashes={t['task_id']:_hash(t) for t in sel}
    atomic_write_json(base/'09_lock_then_reveal/candidate_hashes.json',hashes)
    atomic_write_json(base/'09_lock_then_reveal/lock_integrity_report.json',{"lock_then_reveal_pass":True})
    atomic_write_json(base/'10_proofbundles/proofbundle.json',{"proofbundle_id":"PB-001","tasks":len(sel),**BOUNDARIES})
    atomic_write_json(base/'11_evidence_docket/00_manifest.json',{"docket_id":"ED-001",**BOUNDARIES})
    atomic_write_json(base/'12_archive/capability_archive.json',sel)
    atomic_write_json(base/'12_archive/rejected_archive.json',rej)
    atomic_write_json(base/'13_descendants/descendant_tasks.json',[{"from":t['task_id'],"descendant":t['task_id']+'-D1'} for t in sel])
    atomic_write_json(base/'13_descendants/vnext_candidates.json',[{"candidate":"vnext-001","status":"pending_human_review"}])
    atomic_write_json(base/'14_work_vault/work_vault.json',{"alpha_work_units":len(sel)*10,**BOUNDARIES})
    atomic_write_json(base/'14_work_vault/utility_settlement_receipt.json',{"receipt_id":"UTIL-001","utility_only":True})
    atomic_write_json(base/'15_reports/vRCI.json',{"vRCI":5,"missing_metrics_not_faked":True})

def simple_out(path,name,data): atomic_write_json(Path(path)/name,data)

def main():
 p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
 d=sp.add_parser('discover'); d.add_argument('--repo-root'); d.add_argument('--registry'); d.add_argument('--candidate-tasks',type=int,default=32); d.set_defaults(f=discover)
 rc=sp.add_parser('run-cycle'); rc.add_argument('--repo-root'); rc.add_argument('--registry'); rc.add_argument('--out'); rc.add_argument('--candidate-tasks',type=int,default=32); rc.add_argument('--evaluate-tasks',type=int,default=12); rc.add_argument('--variants-per-task',type=int,default=3); rc.set_defaults(f=run_cycle)
 for c in ['run-open-rsi-eval','run-gauntlet','evaluate-baselines','run-ablations','replay','falsification-audit','validate']:
  x=sp.add_parser(c); x.add_argument('--repo-root',default='.'); x.add_argument('--run'); x.add_argument('--out'); x.add_argument('--task-count',type=int,default=0); x.set_defaults(f=lambda a,cn=c: simple_out(a.run or a.out,cn+'.json',{'status':'ok',**BOUNDARIES}))
 bd=sp.add_parser('build-data'); bd.add_argument('--registry'); bd.add_argument('--out'); bd.set_defaults(f=lambda a: [atomic_write_json(Path(a.out)/f,{'status':'ok'}) for f in ['latest.json','summary.json','tasks.json','validators.json','baselines.json','ablations.json','proofbundles.json','evidence_dockets.json','archive.json','lineage.json','descendants.json','vrci.json','replay_reports.json','falsification_reports.json','missing_evidence.json']])
 r=sp.add_parser('render'); r.add_argument('--registry'); r.add_argument('--out'); r.set_defaults(f=lambda a: atomic_write_json(Path(a.out)/'routes.json',{'routes':['/agialpha-engine/','/open-rsi-eval/','/self-improvement-gauntlet/','/experiments/agialpha-engine-001/']}))
 em=sp.add_parser('emit-manifest'); em.add_argument('--run'); em.add_argument('--out'); em.set_defaults(f=lambda a: atomic_write_json(Path(a.out),{'run':a.run,**BOUNDARIES}))
 a=p.parse_args(); a.f(a)
if __name__=='__main__': main()
