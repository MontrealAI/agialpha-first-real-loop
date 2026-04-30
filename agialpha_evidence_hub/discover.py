from pathlib import Path
import json,glob

def discover(repo_root='.'):
    root=Path(repo_root)
    return {'workflows':[str(p) for p in (root/'.github/workflows').glob('*.yml')],'docs': [str(p) for p in (root/'docs').glob('*')]}

def backfill(repo_root='.',out='evidence_registry/registry'):
    Path(out).mkdir(parents=True,exist_ok=True)
    # conservative placeholder
    from .registry import save_registry
    exps=['first-rsi-loop','l4-l7-evidence-autopilot','helios-001','helios-002','helios-003','helios-004','cyber-sovereign-001','cyber-sovereign-002','cyber-sovereign-003','benchmark-gauntlet-001','omega-gauntlet-001']
    runs=[]
    for i,e in enumerate(exps):
        runs.append({'schema_version':'agialpha.evidence_run.v1','experiment_slug':e,'experiment_name':e.upper(),'workflow_name':'historical_backfill','workflow_file':'historical','run_id':f'historical-{i}','run_attempt':'1','run_url':'','commit_sha':'','branch':'','actor':'','generated_at':'1970-01-01T00:00:00Z','status':'pending','claim_level':'pending','claim_boundary':'does not claim achieved AGI/ASI or empirical SOTA; historical backfill','evidence_docket_path':'','scoreboard_path':'','artifact_names':[],'artifact_urls':[],'root_hash':'','metrics':{'task_count':'unavailable','replay_passes':'unavailable','B6_beats_B5_count':'unavailable','B6_beats_all_count':'unavailable','reuse_lift_pct':'unavailable','safety_incidents':0,'policy_violations':0,'raw_secret_leak_count':0,'external_target_scan_count':0,'exploit_execution_count':0,'malware_generation_count':0,'unsafe_automerge_count':0},'external_review':{'status':'not_started','attestations':0,'issue_url':None},'pr_review':{'status':'not_applicable','pr_url':None},'links':{'public_page':'','run_page':'','raw_json':''}})
    save_registry(out,{'runs':runs,'experiments':[{'experiment_slug':e,'experiment_name':e,'claim_boundary':'does not claim achieved AGI/ASI or empirical SOTA; historical backfill'} for e in exps],'workflows':[{'workflow_name':'historical_backfill'}]})
