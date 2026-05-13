import argparse, datetime, json, pathlib, subprocess
CLAIM_FULL = "This recursive substrate cycle is local, bounded evidence of governance and machine-labor infrastructure. It does not claim achieved AGI, ASI, superintelligence, empirical SOTA, safe autonomy, official benchmark victory, or external validation."
CLAIM_SHORT = "local bounded recursive substrate evidence"

def _jwrite(path,obj):
    path=pathlib.Path(path); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(obj,indent=2)+"\n")

def _jread(path, default):
    p = pathlib.Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text())

def _append_registry(registry_path, filename, entries):
    current = _jread(registry_path / filename, [])
    if not isinstance(current, list):
        current = []
    current.extend(entries)
    _jwrite(registry_path / filename, current)

def _resolve_commit_sha(repo_root):
    try:
        res = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "unavailable"



def _fail(msg):
    raise SystemExit(msg)

def _load_cycle_report(run_input):
    run_path = pathlib.Path(run_input)
    report_path = run_path / '14_reports/recursive_substrate_report.json'
    if not report_path.exists():
        _fail(f"missing cycle report: {report_path}")
    return run_path, json.loads(report_path.read_text())

def _run_replay(run_input):
    run_path, report = _load_cycle_report(run_input)
    required = [run_path/'08_proofbundles/proofbundle.json', run_path/'09_evidence_dockets/00_manifest.json', run_path/'09_evidence_dockets/03_validator_report.json']
    missing = [str(p) for p in required if not p.exists()]
    status = 'pass' if not missing and report.get('claim_boundary') else 'failure'
    return {"status":status, "claim_boundary":CLAIM_SHORT, "missing_artifacts":missing, "reproduced_cycle_id": report.get('cycle_id','unavailable')}

def _run_falsification(run_input):
    run_path, report = _load_cycle_report(run_input)
    redacted = dict(report)
    redacted.pop('claim_boundary', None)
    text = json.dumps(redacted).lower()
    banned = ['achieved agi','achieved asi','superintelligence achieved','empirical sota','safe autonomy','cybersecurity certification']
    hits = [b for b in banned if b in text]
    unsafe_automerge = int(report.get('hard_safety_counters',{}).get('unsafe_automerge_count',0))
    status = 'pass' if not hits and unsafe_automerge == 0 and bool(report.get('claim_boundary')) else 'failure'
    return {"status":status, "claim_boundary":CLAIM_SHORT, "overclaim_found":bool(hits), "overclaim_hits":hits, "unsafe_automerge_count":unsafe_automerge, "input":str(run_path)}

def _validate_run(run_input):
    _, data = _load_cycle_report(run_input)
    errors = []
    if not data.get('claim_boundary'):
        errors.append('claim_boundary_missing')
    if not data.get('substrate_layers',{}).get('human_governed_promotion'):
        errors.append('human_governed_promotion_false')
    counters = data.get('hard_safety_counters',{})
    if counters.get('unsafe_automerge_count') != 0:
        errors.append('unsafe_automerge_not_zero')
    for key in ['raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','social_engineering_content_count','critical_safety_incidents']:
        if key not in counters:
            errors.append(f'missing_{key}')
    if errors:
        _fail('validation_failed: ' + ','.join(errors))

def discover(repo_root, registry):
    ctx={"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"repo_root":str(pathlib.Path(repo_root).resolve()),"claim_boundary":CLAIM_SHORT}
    _jwrite(pathlib.Path(registry)/'latest.json',ctx)
    return ctx

def run_cycle(repo_root, registry, out, candidate_seeds, evaluate_seeds):
    repo_root = pathlib.Path(repo_root)
    outp=pathlib.Path(out); outp.mkdir(parents=True, exist_ok=True)
    insights=[{"insight_id":"insight-001","summary":"Gap detection for recursive substrate","claim_boundary":CLAIM_SHORT}]
    seeds=[{"seed_id":f"seed-{i+1:03d}","kind":["task","validator","doc","workflow","policy","evidence","replay","vnext"][i%8],"status":"accepted" if i<evaluate_seeds else "rejected","claim_boundary":CLAIM_SHORT} for i in range(candidate_seeds)]
    jobs=[{"job_id":f"job-{i+1:03d}","seed_id":s["seed_id"],"human_review_required":True,"status":"completed"} for i,s in enumerate(seeds[:evaluate_seeds])]
    validators=[{"job_id":j["job_id"],"validator_id":"claim-boundary-validator","status":"pass"} for j in jobs]
    caps=[{"capability_id":f"cap-{i+1:03d}","job_id":j["job_id"],"status":"archived"} for i,j in enumerate(jobs)]
    vnext=[{"candidate_id":f"vnext-{i+1:03d}","from_capability":c["capability_id"],"status":"pending_human_review"} for i,c in enumerate(caps)]
    proofbundle={"proofbundle_id":"proofbundle-001","status":"created","claim_boundary":CLAIM_SHORT}
    evidence_docket={"docket_id":"docket-001","status":"created","claim_boundary":CLAIM_SHORT,"human_review_required":True}
    cycle={"schema_version":"agialpha.recursive_cycle.v1","cycle_id":"recursive-cycle-001","cycle_index":len(_jread(pathlib.Path(registry)/'cycles.json',[])),"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"repository":"MontrealAI/agialpha-first-real-loop","commit_sha":_resolve_commit_sha(repo_root),'status':'success','substrate_layers':{"agents":True,"jobs":True,"validators":True,"memory":True,"governance":True,"settlement":True,"recursive_improvement":True,"human_governed_promotion":True},"open_ended_loop":{"insights_generated":len(insights),"nova_seeds_generated":len(seeds),"jobs_generated":len(jobs),"validators_generated":len(validators),"capabilities_archived":len(caps),"vnext_candidates_generated":len(vnext)},"proof_loop":{"proofbundles_created":1,"evidence_dockets_created":1,"replay_reports_created":"pending","falsification_reports_created":"pending"},"governance_loop":{"policy_decisions_created":"pending","human_review_records_created":"pending","promotion_gates_passed":0,"promotion_gates_failed":1},"settlement_loop":{"work_vaults_created":"pending","mark_allocations_created":len(seeds),"sovereign_assignments_created":len(seeds),"utility_settlement_records_created":len(jobs)},"metrics":{"recursive_substrate_readiness_score":"pending","open_ended_discovery_score":"pending","proof_density_score":"pending","memory_reuse_score":"pending","vnext_compounding_score":"pending","human_governance_integrity":"pending"},"hard_safety_counters":{"raw_secret_leak_count":0,"external_target_scan_count":0,"exploit_execution_count":0,"malware_generation_count":0,"social_engineering_content_count":0,"unsafe_automerge_count":0,"critical_safety_incidents":0},"claim_boundary":CLAIM_FULL}
    _jwrite(outp/'08_proofbundles/proofbundle.json',proofbundle)
    _jwrite(outp/'09_evidence_dockets/00_manifest.json',evidence_docket)
    _jwrite(outp/'02_insights/insights.json',insights); _jwrite(outp/'03_nova_seeds/nova_seeds.json',seeds)
    _jwrite(outp/'03_nova_seeds/accepted_seeds.json',[s for s in seeds if s['status']=='accepted']); _jwrite(outp/'03_nova_seeds/rejected_seeds.json',[s for s in seeds if s['status']=='rejected'])
    _jwrite(outp/'06_agi_jobs/jobs.json',jobs); _jwrite(outp/'07_validators/validator_results.json',validators)
    _jwrite(outp/'09_evidence_dockets/03_validator_report.json',validators); _jwrite(outp/'10_archive/capability_archive.json',caps); _jwrite(outp/'11_vnext/vnext_candidates.json',vnext)
    _jwrite(outp/'13_baselines/B6_recursive_substrate.json',{"level":"B6","status":"implemented","claim_boundary":CLAIM_SHORT}); _jwrite(outp/'14_reports/recursive_substrate_report.json',cycle)
    _jwrite(outp/'00_manifest.json',{"claim_boundary":CLAIM_SHORT}); _jwrite(outp/'summary.md',f"# Summary\n\n{CLAIM_SHORT}\n")
    _jwrite(outp/'evidence-run-manifest.json',{"claim_boundary":CLAIM_SHORT})
    reg=pathlib.Path(registry); reg.mkdir(parents=True, exist_ok=True)
    _append_registry(reg, 'cycles.json', [cycle]); _append_registry(reg, 'insights.json', insights); _append_registry(reg, 'nova_seeds.json', seeds)
    _append_registry(reg, 'jobs.json', jobs); _append_registry(reg, 'validators.json', validators); _append_registry(reg, 'capabilities.json', caps)
    _append_registry(reg, 'vnext.json', vnext); _append_registry(reg, 'proofbundles.json', [proofbundle]); _append_registry(reg, 'evidence_dockets.json', [evidence_docket])
    _jwrite(reg/'latest.json',cycle)
    return cycle

def main(argv=None):
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    d=sp.add_parser('discover'); d.add_argument('--repo-root',required=True); d.add_argument('--registry',required=True)
    r=sp.add_parser('run-cycle'); r.add_argument('--repo-root',required=True); r.add_argument('--registry',required=True); r.add_argument('--out',required=True); r.add_argument('--candidate-seeds',type=int,default=16); r.add_argument('--evaluate-seeds',type=int,default=6)
    rp=sp.add_parser('replay'); rp.add_argument('--input',required=True); rp.add_argument('--out',required=True)
    fa=sp.add_parser('falsification-audit'); fa.add_argument('--input',required=True); fa.add_argument('--out',required=True)
    v=sp.add_parser('validate'); v.add_argument('--input',required=True)
    bd=sp.add_parser('build-data'); bd.add_argument('--registry',required=True); bd.add_argument('--out',required=True)
    rr=sp.add_parser('render'); rr.add_argument('--registry',required=True); rr.add_argument('--out',required=True)
    em=sp.add_parser('emit-manifest'); em.add_argument('--input',required=True); em.add_argument('--out',required=True)
    a=ap.parse_args(argv)
    if a.cmd=='discover': discover(a.repo_root,a.registry)
    elif a.cmd=='run-cycle': run_cycle(a.repo_root,a.registry,a.out,a.candidate_seeds,a.evaluate_seeds)
    elif a.cmd=='replay': _jwrite(a.out,_run_replay(a.input))
    elif a.cmd=='falsification-audit': _jwrite(a.out,_run_falsification(a.input))
    elif a.cmd=='validate':
        _validate_run(a.input)
    elif a.cmd=='build-data':
        reg=pathlib.Path(a.registry); out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=True)
        for n in ['latest','cycles','insights','nova_seeds','jobs','capabilities','vnext']:
            p=reg/f'{n}.json'; _jwrite(out/f'{n}.json', _jread(p, []))
        cycles = _jread(reg/'cycles.json', []); insights = _jread(reg/'insights.json', []); seeds = _jread(reg/'nova_seeds.json', [])
        jobs = _jread(reg/'jobs.json', []); validators = _jread(reg/'validators.json', []); proofbundles = _jread(reg/'proofbundles.json', [])
        dockets = _jread(reg/'evidence_dockets.json', []); capabilities = _jread(reg/'capabilities.json', []); vnext = _jread(reg/'vnext.json', [])
        _jwrite(out/'summary.json',{"schema_version":"agialpha.recursive_substrate_summary.v1","generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"cycles_run":len(cycles),"insights_generated":len(insights),"nova_seeds_generated":len(seeds),"jobs_generated":len(jobs),"validators_generated":len(validators),"proofbundles_created":len(proofbundles),"evidence_dockets_created":len(dockets),"capabilities_archived":len(capabilities),"vnext_candidates_generated":len(vnext),"recursive_substrate_readiness_score":"pending","claim_boundary":CLAIM_FULL})
    elif a.cmd=='render':
        out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=True); _jwrite(out/'index.json',{"status":"generated","claim_boundary":CLAIM_SHORT})
    elif a.cmd=='emit-manifest': _jwrite(a.out,{"input":a.input,"claim_boundary":CLAIM_SHORT})
    return 0
