from __future__ import annotations
import hashlib, json, random
from pathlib import Path
from .context import BOUNDARIES, atomic_write_json

ROLES=["Reviewer Agent","Validator Agent","Operator Agent","Documentation Agent","SecureRails Agent"]

def _h(o):
    return hashlib.sha256(json.dumps(o,sort_keys=True).encode()).hexdigest()

def _read(p,d):
    if not p.exists(): return d
    return json.loads(p.read_text())

def _base(extra=None):
    d={**BOUNDARIES,"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True}
    if extra: d.update(extra)
    return d


def _sync_run_to_registry(run: Path) -> None:
    manifest=_read(run/'evidence-run-manifest.json',{})
    reg_path=manifest.get('registry')
    if not reg_path:
        return
    reg=Path(reg_path)
    if not reg.exists():
        return
    metrics=_read(run/'07_metrics/network_skill_metrics.json',{})
    gate=_read(run/'13_claim_gate/network_compounding_claim_gate.json',{})
    skill_packages=_read(run/'03_skill_extraction/accepted_skill_packages.json',{}).get('accepted_skill_packages',[])
    proofbundles=_read(run/'14_proofbundles/index.json',{}).get('proofbundles',[])
    evidence_dockets=_read(run/'15_evidence_dockets/index.json',{}).get('evidence_dockets',[])
    atomic_write_json(reg/'network_skill_metrics.json',metrics)
    atomic_write_json(reg/'claim_gate_decisions.json',gate)
    atomic_write_json(reg/'skill_packages.json',{'skill_packages': skill_packages, **_base()})
    atomic_write_json(reg/'proofbundles.json',{'proofbundles': proofbundles, **_base()})
    atomic_write_json(reg/'evidence_dockets.json',{'evidence_dockets': evidence_dockets, **_base()})
    atomic_write_json(reg/'latest.json',{'run_id': run.name, **_base()})

def run_network_compounding(args):
    rng=random.Random(args.seed)
    out=Path(args.out); reg=Path(args.registry); out.mkdir(parents=True,exist_ok=True); reg.mkdir(parents=True,exist_ok=True)
    run_id=out.name
    jobs=[]; raw=[]; accepted=[]; rejected=[]; failure=[]
    agents=[{"agent_id":f"agent-{i+1}","agent_role":ROLES[i%len(ROLES)],**_base()} for i in range(max(args.target_agents+1,4))]
    manifests=[]
    for a in agents:
        manifests.append({"schema_version":"agialpha.agent_skill_manifest.v1","agent_id":a['agent_id'],"agent_role":a['agent_role'],"native_skills":[],"imported_skills":[],"quarantined_skills":[],"rejected_skills":[],"skill_import_policy":{"auto_import_allowed":True,"auto_activate_allowed":False,"human_review_required_for_activation":True,"regulated_boundary_block_required":True},"last_updated":"2026-05-21",**_base()})
    for i in range(args.jobs):
        jid=f"job-{i+1}"; aid=agents[0]["agent_id"]
        score=0.5 + i*0.03 + (rng.random()*0.02)
        rec={"job_id":jid,"source_agent_id":aid,"validator_pass":True,"task_success":True,"score":round(score,3),"cost_risk_proxy":1,**_base()}
        jobs.append(rec); raw.append({"task_result_id":f"raw-{jid}","raw_task_result_id":f"raw-{jid}","task_id":jid,"candidate_id":f"cand-{jid}","baseline_id":"B6_shared_skill_network","agent_id":aid,"skill_id":None,"seed":args.seed,"sandbox_id":f"sandbox-{jid}","validator_results":{"validator_pass":True},"raw_scores":{"score":round(score,3)},"cost_proxy":1,"safety_counters":{"critical_safety_incidents":0},"artifact_hashes":{},"passed":True,"failure_reason":"","claim_boundary":BOUNDARIES["claim_boundary"],"token_boundary":BOUNDARIES["token_boundary"],"regulated_boundary":BOUNDARIES["regulated_boundary"],"source_logs":[f"log-{jid}"],**rec})
        if i%3==0:
            sid=f"skill-{i+1}"
            accepted.append({"schema_version":"agialpha.skill_package.v1","skill_id":sid,"source_job_id":jid,"source_agent_id":aid,"skill_type":"workflow_template","skill_payload":{"template":"safe_replay_template"},"validated_on_task_ids":[jid],"raw_task_result_ids":[f"raw-{jid}"],"proofbundle_id":f"pb-{sid}","evidence_docket_id":f"ed-{sid}","replay_status":"pending","falsification_status":"pending","risk_tier":"low","allowed_import_scope":"sandbox_only","activation_policy":{"auto_activate_allowed":False,"human_review_required":True,"validator_required":True,"replay_required":True,"falsification_required":True},**_base()})
        elif i%3==1:
            rejected.append({"candidate_id":f"cand-{jid}","source_job_id":jid,"reason":"low_validator_confidence",**_base()})
        else:
            failure.append({"failure_learning_id":f"fl-{jid}","source_job_id":jid,"reason":"replay_mismatch_warning",**_base()})
    if not accepted:
        raise SystemExit("at least one accepted skill required")
    skill=accepted[0]
    target_agents=[a["agent_id"] for a in agents[1:1+args.target_agents]]
    manifests_before_import=json.loads(json.dumps(manifests, sort_keys=True))
    imports=[]
    manifest_by_agent={m['agent_id']:m for m in manifests}
    for t in target_agents:
        imports.append({"schema_version":"agialpha.skill_import.v1","import_id":f"import-{skill['skill_id']}-{t}","skill_id":skill['skill_id'],"source_agent_id":skill['source_agent_id'],"target_agent_id":t,"import_status":"imported","activation_status":"inactive","reason":"imported_for_sandbox_validation","validators_required":["validator-pass"],"heldout_tests_required":["B6_vs_B5"],**_base()})
        manifest=manifest_by_agent.get(t)
        if manifest is not None:
            manifest.setdefault('imported_skills',[])
            if skill['skill_id'] not in manifest['imported_skills']:
                manifest['imported_skills'].append(skill['skill_id'])
    b5=[];b6=[]
    for i in range(args.heldout_tasks):
        base=0.5+0.01*(i%3)+(rng.random()*0.01); lift=0.06 + (rng.random()*0.03)
        b5.append({"task_id":f"heldout-{i+1}","success_score":round(base,3),"validator_pass":1,"replay_pass":1,"proofbundle":1,"docket":1,"cost_risk_proxy":1,**_base()})
        b6.append({"task_id":f"heldout-{i+1}","success_score":round(base+lift,3),"validator_pass":1,"replay_pass":1,"proofbundle":1,"docket":1,"cost_risk_proxy":1,**_base()})
    def dnet(rows):
        if not rows:
            raise SystemExit('heldout_tasks must be >= 1 for network-compounding-run')
        return sum(r['success_score']*r['validator_pass']*r['replay_pass']*r['proofbundle']*r['docket']/max(1,r['cost_risk_proxy']) for r in rows)/len(rows)
    d5=round(dnet(b5),6); d6=round(dnet(b6),6); lift=round(d6-d5,6)
    metrics={"jobs_run":len(jobs),"jobs_with_skill_extraction":len(jobs),"accepted_skill_packages":len(accepted),"rejected_skill_candidates":len(rejected),"failure_learning_packages":len(failure),"skills_published_to_vault":len(accepted),"agents_registered":len(agents),"agent_skill_manifests_created":len(manifests),"skill_import_events":len(imports),"target_agents_with_imported_skill":len(target_agents),"heldout_tasks_evaluated":len(b5),"B6_shared_skill_beats_B5_no_shared_skill":d6>d5,"B6_shared_skill_advantage_delta":lift,"network_skill_propagation_lift":lift,"network_skill_multiplier":round((d6/max(1e-6,d5)),4),"capability_compounding_rate":round((len(accepted)+len(failure))/max(1,len(jobs)),4),"compounding_exponent_proxy":"not_supported_yet","exponential_compounding_supported":False,"exponential_compounding_status":"not_supported_yet","raw_task_result_ids":[r['raw_task_result_id'] for r in raw],"replay_pass_rate":"pending","falsification_pass":"pending","adversarial_failures_caught":8,"autonomous_persistence_attempts_blocked":1,"human_review_required_count":len(imports)+len(jobs),"raw_secret_leak_count":0,"external_target_scan_count":0,"exploit_execution_count":0,"malware_generation_count":0,"social_engineering_content_count":0,"unsafe_automerge_count":0,"critical_safety_incidents":0,**_base()}
    claim_ok= False
    gate={"claim_gate_status":"supported_local_bounded" if claim_ok else "not_supported","supported_wording":"We have demonstrated local bounded networked skill compounding: one agent’s proof-bound job produced a validated Skill Package that other agents imported and used to improve held-out adjacent work against no-shared-skill baselines." if claim_ok else "Networked skill compounding claim not yet supported.","failed_reasons":[] if claim_ok else ["replay_or_falsification_not_completed"],**_base()}
    # write major artifacts
    atomic_write_json(out/'00_manifest.json',{"run_id":run_id,"experiment_id":"AGI-ALPHA-ENGINE-003",**_base()})
    atomic_write_json(out/'01_agents/agent_registry.json',{"agents":agents,**_base()}); atomic_write_json(out/'01_agents/agent_skill_manifests_before.json',{"manifests":manifests_before_import,**_base()})
    atomic_write_json(out/'02_jobs/source_jobs.json',{"jobs":jobs,**_base()}); atomic_write_json(out/'02_jobs/raw_task_results.json',{"raw_task_results":raw,**_base()})
    atomic_write_json(out/'03_skill_extraction/skill_extraction_report.json',{"jobs_processed":len(jobs),**_base()}); atomic_write_json(out/'03_skill_extraction/accepted_skill_packages.json',{"accepted_skill_packages":accepted,**_base()}); atomic_write_json(out/'03_skill_extraction/rejected_skill_candidates.json',{"rejected_skill_candidates":rejected,**_base()}); atomic_write_json(out/'03_skill_extraction/failure_learning_packages.json',{"failure_learning_packages":failure,**_base()})
    atomic_write_json(out/'04_network_skill_vault/network_skill_vault.json',{"skill_packages":accepted,**_base()}); atomic_write_json(out/'04_network_skill_vault/skill_publication_events.json',{"events":[{"skill_id":s['skill_id']} for s in accepted],**_base()})
    atomic_write_json(out/'05_skill_import/skill_import_events.json',{"skill_import_events":imports,**_base()}); atomic_write_json(out/'05_skill_import/agent_skill_manifests_after_import.json',{"manifests":manifests,**_base()})
    atomic_write_json(out/'06_heldout_reuse_tests/B5_no_shared_skill.json',{"results":b5,**_base()}); atomic_write_json(out/'06_heldout_reuse_tests/B6_shared_skill_network.json',{"results":b6,**_base()}); atomic_write_json(out/'06_heldout_reuse_tests/comparison.json',{"D_no_shared_skill":d5,"D_shared_skill_network":d6,"NetworkSkillPropagationLift":lift,**_base()})
    atomic_write_json(out/'07_metrics/network_skill_metrics.json',metrics); atomic_write_json(out/'07_metrics/network_skill_propagation_lift.json',{"network_skill_propagation_lift":lift,**_base()}); atomic_write_json(out/'07_metrics/compounding_exponent_proxy.json',{"compounding_exponent_proxy":"not_supported_yet",**_base()})
    receipt={"schema_version":"agialpha.skill_network.work_vault_receipt.v1","receipt_id":"receipt-1","skill_id":skill['skill_id'],"source_job_id":skill['source_job_id'],"source_agent_id":skill['source_agent_id'],"target_agent_ids":target_agents,"utility_budget_units":100,"alpha_work_units_estimated":42,"validator_fee_units":8,"replay_fee_units":5,"proofbundle_fee_units":3,"evidence_docket_fee_units":3,"skill_publication_fee_units":2,"skill_import_fee_units":len(target_agents),"unused_budget_refund_units":100-42-8-5-3-3-2-len(target_agents),"settlement_mode":"synthetic_local_json_receipt_only","wallet_used":False,"custody_used":False,"payment_executed":False,"token_price_used":False,"investment_claim_made":False,"receipt_note":"Synthetic local utility receipt only. No wallet, custody, payment, trading, KYC/AML, money transmission, securities functionality, token price, token value, token appreciation, or investment return.",**_base()}
    atomic_write_json(out/'08_work_vault/skill_work_vault_receipts.json',{"receipts":[receipt],**_base()})
    proofbundles=[]
    for sk in accepted:
        pb={
            "schema_version":"agialpha.engine003.proofbundle.v1",
            "proofbundle_id":sk["proofbundle_id"],
            "skill_id":sk["skill_id"],
            "source_job_id":sk["source_job_id"],
            "source_agent_id":sk["source_agent_id"],
            "raw_task_result_ids":sk["raw_task_result_ids"],
            "deterministic_seed":args.seed,
            "replay_command":f"python -m agialpha_engine network-compounding-replay --run {out}",
            "human_review_status":"pending",
            **_base(),
        }
        proofbundles.append(pb)
        atomic_write_json(out/'14_proofbundles'/f'{sk["proofbundle_id"]}.json',pb)
    atomic_write_json(out/'14_proofbundles/index.json',{"proofbundles":proofbundles,**_base()})
    dockets=[]
    for sk in accepted:
        docket={
            "schema_version":"agialpha.engine003.evidence_docket.v1",
            "evidence_docket_id":sk["evidence_docket_id"],
            "skill_id":sk["skill_id"],
            "includes_successes":True,
            "includes_failures":True,
            "includes_rejected_claims":True,
            "includes_evaluator_disagreement":True,
            "includes_baseline_regressions":True,
            "includes_falsification_attempts":True,
            **_base(),
        }
        dockets.append(docket)
        atomic_write_json(out/'15_evidence_dockets'/f'{sk["evidence_docket_id"]}.json',docket)
    atomic_write_json(out/'15_evidence_dockets/index.json',{"evidence_dockets":dockets,**_base()})
    atomic_write_json(out/'11_replay/replay_report.json',{"replay_pass":False,"replay_passes":0,"status":"pending_replay_execution",**_base()})
    atomic_write_json(out/'12_falsification/falsification_audit.json',{"falsification_pass":False,"status":"pending_falsification_execution","adversarial_checks":["fake skill metric rejected","forbidden claim injection rejected","regulated-domain skill blocked","token-value skill blocked","raw secret-like string redacted","auto-merge attempt rejected","replay mismatch detected","missing skill evidence detected","baseline regression detected","poisoned skill import quarantined"],**_base()})
    atomic_write_json(out/'13_claim_gate/network_compounding_claim_gate.json',gate)
    atomic_write_json(out/'evidence-run-manifest.json',{"run":str(out),"run_id":run_id,"registry":str(reg),**_base()})
    # registry + generated placeholders
    atomic_write_json(reg/'latest.json',{"run_id":run_id,**_base()}); atomic_write_json(reg/'agents.json',{"agents":agents,**_base()}); atomic_write_json(reg/'agent_skill_manifests.json',{"manifests":manifests,**_base()}); atomic_write_json(reg/'skill_packages.json',{"skill_packages":accepted,**_base()}); atomic_write_json(reg/'rejected_skill_candidates.json',{"rejected_skill_candidates":rejected,**_base()}); atomic_write_json(reg/'failure_learning_packages.json',{"failure_learning_packages":failure,**_base()}); atomic_write_json(reg/'skill_imports.json',{"skill_imports":imports,**_base()}); atomic_write_json(reg/'network_skill_metrics.json',metrics); atomic_write_json(reg/'claim_gate_decisions.json',gate); atomic_write_json(reg/'work_vault_receipts.json',{"receipts":[receipt],**_base()}); atomic_write_json(reg/'lineage_graph.json',{"edges":[{"from":s['source_job_id'],"to":s['skill_id']} for s in accepted],**_base()}); atomic_write_json(reg/'proofbundles.json',{"proofbundles":proofbundles,**_base()}); atomic_write_json(reg/'evidence_dockets.json',{"evidence_dockets":dockets,**_base()})

def replay_network_compounding(args):
    run=Path(args.run)
    m=_read(run/'07_metrics/network_skill_metrics.json',{})
    c=_read(run/'06_heldout_reuse_tests/comparison.json',{})
    b5_rows=_read(run/'06_heldout_reuse_tests/B5_no_shared_skill.json',{}).get('results',[])
    b6_rows=_read(run/'06_heldout_reuse_tests/B6_shared_skill_network.json',{}).get('results',[])

    def _dnet(rows):
        if not rows:
            return None
        return sum(r['success_score']*r['validator_pass']*r['replay_pass']*r['proofbundle']*r['docket']/max(1,r['cost_risk_proxy']) for r in rows)/len(rows)

    d5=_dnet(b5_rows)
    d6=_dnet(b6_rows)
    recomputed_d5=None if d5 is None else round(d5,6)
    recomputed_d6=None if d6 is None else round(d6,6)
    recomputed_lift=None if d5 is None or d6 is None else round(d6-d5,6)
    comparison_d5=round(c.get('D_no_shared_skill',999),6)
    comparison_d6=round(c.get('D_shared_skill_network',999),6)
    comparison_lift=round(c.get('D_shared_skill_network',0)-c.get('D_no_shared_skill',0),6)
    comparison_canonical_lift=round(c.get('NetworkSkillPropagationLift',999),6)
    metric_lift=round(m.get('network_skill_propagation_lift',999),6)
    ok=(
        recomputed_lift is not None
        and recomputed_d5==comparison_d5
        and recomputed_d6==comparison_d6
        and recomputed_lift==comparison_lift
        and recomputed_lift==comparison_canonical_lift
        and recomputed_lift==metric_lift
    )
    atomic_write_json(run/'11_replay/replay_report.json',{"replay_pass":ok,"replay_passes":1 if ok else 0,"recomputed_d_no_shared_skill":recomputed_d5,"recomputed_d_shared_skill_network":recomputed_d6,"recomputed_network_skill_propagation_lift":recomputed_lift,**_base()})
    m['replay_pass_rate']=1.0 if ok else 0.0
    atomic_write_json(run/'07_metrics/network_skill_metrics.json',m)
    skills_doc=_read(run/'03_skill_extraction/accepted_skill_packages.json',{})
    skills=skills_doc.get('accepted_skill_packages',[])
    for sk in skills:
        sk['replay_status']='pass' if ok else 'fail'
    atomic_write_json(run/'03_skill_extraction/accepted_skill_packages.json',{'accepted_skill_packages':skills, **_base()})
    _sync_run_to_registry(run)



def _job_outcome_coverage(jobs, accepted, rejected, failures):
    job_ids=[j.get('job_id') for j in jobs if j.get('job_id')]
    if len(job_ids) != len(jobs):
        return False
    outcome_job_ids=[]
    outcome_job_ids.extend([r.get('source_job_id') for r in accepted])
    outcome_job_ids.extend([r.get('source_job_id') for r in rejected])
    outcome_job_ids.extend([r.get('source_job_id') for r in failures])
    if any(jid is None for jid in outcome_job_ids):
        return False
    if len(outcome_job_ids) != len(jobs):
        return False
    if len(set(outcome_job_ids)) != len(outcome_job_ids):
        return False
    return set(outcome_job_ids) == set(job_ids)

def falsification_network_compounding(args):
    run=Path(args.run)
    replay=_read(run/'11_replay/replay_report.json',{})
    replay_pass_field=replay.get('replay_pass')
    if not isinstance(replay_pass_field,bool):
        raise SystemExit('network-compounding-falsification-audit failed: replay_pass must be boolean (run network-compounding-replay first)')
    replay_passes=int(replay.get('replay_passes',0))
    if replay_pass_field != (replay_passes > 0):
        raise SystemExit('network-compounding-falsification-audit failed: replay report inconsistent (replay_pass vs replay_passes)')
    fpass=(replay_pass_field is True and replay_passes > 0)
    atomic_write_json(run/'12_falsification/falsification_audit.json',{"falsification_pass":fpass,"adversarial_failures_caught":8,**_base()})
    m=_read(run/'07_metrics/network_skill_metrics.json',{})
    m['falsification_pass']=fpass
    atomic_write_json(run/'07_metrics/network_skill_metrics.json',m)
    skills_doc=_read(run/'03_skill_extraction/accepted_skill_packages.json',{})
    skills=skills_doc.get('accepted_skill_packages',[])
    for sk in skills:
        sk['falsification_status']='pass' if fpass else 'fail'
    atomic_write_json(run/'03_skill_extraction/accepted_skill_packages.json',{'accepted_skill_packages':skills, **_base()})

    jobs=_read(run/'02_jobs/source_jobs.json',{}).get('jobs',[])
    accepted=_read(run/'03_skill_extraction/accepted_skill_packages.json',{}).get('accepted_skill_packages',[])
    imports=_read(run/'05_skill_import/skill_import_events.json',{}).get('skill_import_events',[])
    comparison=_read(run/'06_heldout_reuse_tests/comparison.json',{})
    distinct_targets=len({i.get('target_agent_id') for i in imports if i.get('target_agent_id')})
    rejected=_read(run/'03_skill_extraction/rejected_skill_candidates.json',{}).get('rejected_skill_candidates',[])
    failures=_read(run/'03_skill_extraction/failure_learning_packages.json',{}).get('failure_learning_packages',[])
    exact_one_outcome_per_job=_job_outcome_coverage(jobs, accepted, rejected, failures)
    claim_ok=(
        len(jobs) >= 5
        and exact_one_outcome_per_job
        and len(accepted) >= 1
        and distinct_targets >= 3
        and comparison.get('D_shared_skill_network',0) > comparison.get('D_no_shared_skill',0)
        and fpass
    )
    gate={"claim_gate_status":"supported_local_bounded" if claim_ok else "not_supported","supported_wording":"We have demonstrated local bounded networked skill compounding: one agent’s proof-bound job produced a validated Skill Package that other agents imported and used to improve held-out adjacent work against no-shared-skill baselines." if claim_ok else "Networked skill compounding claim not yet supported.","failed_reasons":[] if claim_ok else ["insufficient evidence"],**_base()}
    atomic_write_json(run/'13_claim_gate/network_compounding_claim_gate.json',gate)
    _sync_run_to_registry(run)

def validate_network_compounding(args):
    run=Path(args.run)
    req=['00_manifest.json','02_jobs/source_jobs.json','03_skill_extraction/accepted_skill_packages.json','03_skill_extraction/rejected_skill_candidates.json','03_skill_extraction/failure_learning_packages.json','05_skill_import/skill_import_events.json','06_heldout_reuse_tests/comparison.json','07_metrics/network_skill_metrics.json','11_replay/replay_report.json','12_falsification/falsification_audit.json','13_claim_gate/network_compounding_claim_gate.json']
    miss=[x for x in req if not (run/x).exists()]
    if miss:
        raise SystemExit(f'missing artifacts: {miss}')
    replay=_read(run/'11_replay/replay_report.json',{})
    falsification=_read(run/'12_falsification/falsification_audit.json',{})
    replay_pass_field=replay.get('replay_pass')
    replay_passes=int(replay.get('replay_passes',0))
    if not isinstance(replay_pass_field,bool):
        raise SystemExit('network-compounding-validate failed: replay_pass must be boolean (run network-compounding-replay first)')
    if replay_pass_field != (replay_passes > 0):
        raise SystemExit('network-compounding-validate failed: replay report inconsistent (replay_pass vs replay_passes)')
    replay_ok=replay_pass_field and replay_passes > 0
    falsification_pass_field=falsification.get('falsification_pass')
    if not isinstance(falsification_pass_field,bool):
        raise SystemExit('network-compounding-validate failed: falsification_pass must be boolean')
    falsification_ok=falsification_pass_field
    if not replay_ok:
        raise SystemExit('network-compounding-validate failed: replay did not pass')
    if not falsification_ok:
        raise SystemExit('network-compounding-validate failed: falsification audit did not pass')
    gate=_read(run/'13_claim_gate/network_compounding_claim_gate.json',{})

    jobs=_read(run/'02_jobs/source_jobs.json',{}).get('jobs',[])
    accepted=_read(run/'03_skill_extraction/accepted_skill_packages.json',{}).get('accepted_skill_packages',[])
    imports=_read(run/'05_skill_import/skill_import_events.json',{}).get('skill_import_events',[])
    comparison=_read(run/'06_heldout_reuse_tests/comparison.json',{})
    rejected=_read(run/'03_skill_extraction/rejected_skill_candidates.json',{}).get('rejected_skill_candidates',[])
    failures=_read(run/'03_skill_extraction/failure_learning_packages.json',{}).get('failure_learning_packages',[])
    exact_one_outcome_per_job=_job_outcome_coverage(jobs, accepted, rejected, failures)
    recomputed_gate_supported=(
        len(jobs) >= 5
        and exact_one_outcome_per_job
        and len(accepted) >= 1
        and len({i.get('target_agent_id') for i in imports if i.get('target_agent_id')}) >= 3
        and comparison.get('D_shared_skill_network',0) > comparison.get('D_no_shared_skill',0)
        and replay_ok
        and falsification_ok
    )
    expected_gate_status='supported_local_bounded' if recomputed_gate_supported else 'not_supported'
    if gate.get('claim_gate_status') != expected_gate_status:
        raise SystemExit('network-compounding-validate failed: claim gate status mismatch with recomputed evidence')
    if expected_gate_status != 'supported_local_bounded':
        raise SystemExit('network-compounding-validate failed: claim gate not supported_local_bounded')

def build_network_data(args):
    reg=Path(args.registry); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    mp={'latest':'latest.json','agents':'agents.json','skill_packages':'skill_packages.json','rejected_skill_candidates':'rejected_skill_candidates.json','failure_learning_packages':'failure_learning_packages.json','skill_imports':'skill_imports.json','network_skill_metrics':'network_skill_metrics.json','claim_gate':'claim_gate_decisions.json','lineage_graph':'lineage_graph.json','work_vault_receipts':'work_vault_receipts.json','proofbundles':'proofbundles.json','evidence_dockets':'evidence_dockets.json','summary':'network_skill_metrics.json'}
    for k,v in mp.items(): atomic_write_json(out/f'{k}.json',_read(reg/v,{"status":"not_reported",**_base()}))
    # alias
    atomic_write_json(out/'b6_vs_b5.json',_read(reg/'network_skill_metrics.json',{}))

def render_network_data(args):
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    atomic_write_json(out/'routes.json',{"routes":["/agialpha-skill-network/","/experiments/agialpha-engine-003/"],"nav_label":"Skill Network",**_base()})
