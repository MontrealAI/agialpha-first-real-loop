import argparse, json
from pathlib import Path
from datetime import datetime, timezone
from .ingest import load_input
from .validate import validate_manifest, validate_registry, validate_site
from .registry import update_registry
from .build import build_site
from .linkcheck import linkcheck
from .discover import discover_to_file
from .workflow_dispatch import parse_workflow_dispatch_inputs, workflow_gh_command
from .needed_update import needed_update
from .repair import generate_repair_plan

def _default_manifest(args):
    return {
      'schema_version':'agialpha.evidence_run.v1','experiment_slug':args.experiment_slug,'experiment_name':args.experiment_name or args.experiment_slug.upper(),'experiment_family':'-'.join(args.experiment_slug.split('-')[:2]),'workflow_name':args.workflow_name or 'unknown','workflow_file':args.workflow_file or 'unknown','run_id':args.run_id,'run_attempt':args.run_attempt or '1','run_url':args.run_url,'commit_sha':args.commit or 'unknown','branch':args.branch or 'unknown','actor':'github-actions','event':'workflow_dispatch','generated_at':datetime.now(timezone.utc).isoformat(),'status':'pending','conclusion':'unknown','claim_level':'pending','claim_boundary':'does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world security certification, guaranteed economic return, or civilization-scale capability.','evidence_docket_path':args.docket,'scoreboard_path':args.scoreboard,'artifact_names':['evidence-run-manifest'],'artifact_ids':[],'artifact_urls':[],'root_hash':'unavailable','source':'manifest','metrics':{k:'not_reported' for k in ['task_count','replay_passes','baseline_count','B6_beats_B5_count','B6_beats_all_count','mean_advantage_delta_vs_B5','reuse_lift_pct','capability_reuse_lift_pct','valid_findings_count','safety_incidents','policy_violations','raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','social_engineering_content_count','unsafe_automerge_count','critical_safety_incidents']},'external_review':{'status':'not_started','attestations':'not_reported','issue_url':None},'pr_review':{'status':'not_applicable','pr_url':None},'links':{'public_page':'/agialpha-first-real-loop/','experiment_page':f"/agialpha-first-real-loop/experiments/{args.experiment_slug}/",'run_page':f"/agialpha-first-real-loop/runs/{args.run_id}/",'raw_json':f"/agialpha-first-real-loop/runs/{args.run_id}/manifest.json"}
    }

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    d=sp.add_parser('discover'); d.add_argument('--repo-root',default='.'); d.add_argument('--out',default='evidence_registry/discovered.json')
    b=sp.add_parser('backfill'); b.add_argument('--repo-root',default='.'); b.add_argument('--registry',default='evidence_registry')
    ia=sp.add_parser('ingest-artifacts'); ia.add_argument('--registry',default='evidence_registry'); ia.add_argument('--runs-dir',required=True)
    r=sp.add_parser('register-run'); r.add_argument('--input', required=True); r.add_argument('--registry',default='evidence_registry')
    gh=sp.add_parser('github-discover'); gh.add_argument('--registry',default='evidence_registry'); gh.add_argument('--limit',type=int,default=500)
    eb=sp.add_parser('emit-manifest'); eb.add_argument('--experiment-slug',required=True); eb.add_argument('--experiment-name'); eb.add_argument('--workflow-name'); eb.add_argument('--workflow-file'); eb.add_argument('--run-id',required=True); eb.add_argument('--run-attempt'); eb.add_argument('--run-url',required=True); eb.add_argument('--commit'); eb.add_argument('--branch'); eb.add_argument('--docket'); eb.add_argument('--scoreboard'); eb.add_argument('--out',required=True)
    bs=sp.add_parser('build'); bs.add_argument('--registry',default='evidence_registry'); bs.add_argument('--out',default='_site')
    vr=sp.add_parser('validate-registry'); vr.add_argument('--registry',default='evidence_registry')
    v=sp.add_parser('validate'); v.add_argument('--registry',default='evidence_registry'); v.add_argument('--site',default='_site')
    l=sp.add_parser('linkcheck'); l.add_argument('--site',default='_site')
    wc=sp.add_parser('workflow-catalog'); wc.add_argument('--repo-root',default='.'); wc.add_argument('--registry',default='evidence_registry')
    nu=sp.add_parser('needed-update'); nu.add_argument('--registry',default='evidence_registry'); nu.add_argument('--repo-root',default='.'); nu.add_argument('--out')
    rp=sp.add_parser('repair'); rp.add_argument('--registry',default='evidence_registry'); rp.add_argument('--repo-root',default='.'); rp.add_argument('--out')
    a=ap.parse_args()
    if a.cmd=='discover': print(json.dumps(discover_to_file(a.repo_root,a.out),indent=2))
    elif a.cmd=='register-run': m=load_input(a.input); validate_manifest(m); update_registry(a.registry,m)
    elif a.cmd=='backfill':
        payload=discover_to_file(a.repo_root, 'evidence_registry/discovered.json')
        for f in payload['discovered_files']:
            if f.endswith('00_manifest.json'):
                m=load_input(Path(a.repo_root)/f)
                slug=(m.get('experiment_slug') or Path(f).parts[-2]).lower().replace('_','-')
                run={'schema_version':'agialpha.evidence_run.v1','experiment_slug':slug,'experiment_name':slug.upper(),'experiment_family':'-'.join(slug.split('-')[:2]),'workflow_name':'historical-backfill','workflow_file':'historical','run_id':f'historical-{slug}','run_url':'https://github.com/MontrealAI/agialpha-first-real-loop/actions','generated_at':datetime.now(timezone.utc).isoformat(),'status':'discovered','conclusion':'unknown','claim_level':'historical-local','claim_boundary':'does not claim achieved AGI, ASI, or empirical SOTA.','source':'historical_backfill','metrics':{k:'unavailable' for k in _default_manifest(type('A',(),{'experiment_slug':slug,'experiment_name':None,'workflow_name':None,'workflow_file':None,'run_id':'x','run_attempt':None,'run_url':'u','commit':None,'branch':None,'docket':None,'scoreboard':None})).get('metrics',{})},'external_review':{'status':'not_started','attestations':'not_reported','issue_url':None},'pr_review':{'status':'not_applicable','pr_url':None},'artifact_names':[],'artifact_ids':[],'artifact_urls':[],'links':{'public_page':'/agialpha-first-real-loop/','experiment_page':f'/agialpha-first-real-loop/experiments/{slug}/','run_page':f'/agialpha-first-real-loop/runs/historical-{slug}/','raw_json':f'/agialpha-first-real-loop/runs/historical-{slug}/manifest.json'}}
                update_registry(a.registry,run)
    elif a.cmd=='emit-manifest': m=_default_manifest(a); Path(a.out).write_text(json.dumps(m,indent=2)); print(a.out)
    elif a.cmd=='build': build_site(a.registry,a.out)
    elif a.cmd=='validate-registry': validate_registry(a.registry)
    elif a.cmd=='validate': validate_registry(a.registry); validate_site(a.site)
    elif a.cmd=='linkcheck': linkcheck(a.site)
    elif a.cmd=='ingest-artifacts': print('0')
    elif a.cmd=='github-discover': print(json.dumps({'limit':a.limit,'runs':[]},indent=2))
    elif a.cmd=='needed-update':
        result=needed_update(a.registry, a.repo_root)
        out_path = Path(a.out) if a.out else Path(a.registry)/'needed_update.json'
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2))
    elif a.cmd=='repair':
        result=generate_repair_plan(a.registry, a.repo_root)
        out_path = Path(a.out) if a.out else Path(a.registry)/'repair_plan.json'
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2))
    elif a.cmd=='workflow-catalog':
        root=Path(a.repo_root)
        rows=[]
        workflow_files = sorted((root/'.github/workflows').glob('*.yml')) + sorted((root/'.github/workflows').glob('*.yaml'))
        for wf in sorted(workflow_files):
            text=wf.read_text()
            has_dispatch='workflow_dispatch' in text
            rows.append({'workflow_file':str(wf.relative_to(root)),'has_workflow_dispatch':has_dispatch,'inputs':parse_workflow_dispatch_inputs(text),'gh_command':workflow_gh_command(str(wf),has_dispatch)})
        out=Path(a.registry)/'workflow_catalog.json'
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps({'workflows':rows},indent=2))
        print(json.dumps({'workflows':rows},indent=2))
if __name__=='__main__': main()
