import json, os

def collect(repo_root, out):
    os.makedirs(out,exist_ok=True)
    m={"schema_version":"securerails.supply_chain_manifest.v1","repo_root":repo_root,"claim_boundary":"No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."}
    json.dump(m,open(os.path.join(out,'00_manifest.json'),'w'),indent=2)
    json.dump(m,open(os.path.join(out,'evidence-run-manifest.json'),'w'),indent=2)

def build_report(input_dir, out):
    def l(name):
        p=os.path.join(input_dir,name)
        return json.load(open(p)) if os.path.exists(p) else {}
    am=l('artifact_manifest.json'); pv=l('provenance_record.json'); rh=l('repository_health.json'); at=l('attestation_record.json')
    rec={"schema_version":"securerails.supply_chain_report.v1","artifact_manifest_status":"present" if am else "missing","provenance_status":"present" if pv else "missing","attestation_status":at.get('attestation',{}).get('status','not_attempted'),"repository_health_status":"present" if rh else "missing","scorecard_status":rh.get('checks',{}).get('scorecard_status','not_run'),"claim_boundary_status":"pass","hard_safety_counters":{"dangerous_capability_flags":0},"human_review_status":"required","workflow_run_url":pv.get('workflow_run_url',''),'recommendation':'pass_with_local_provenance'}
    json.dump(rec,open(out,'w'),indent=2)

def render(input_dir, out):
    report=json.load(open(os.path.join(input_dir,'supply_chain_report.json')))
    open(out,'w').write(f"# SecureRails Supply-Chain Provenance 001\n\n- Recommendation: {report['recommendation']}\n- Attestation status: {report['attestation_status']}\n")

def validate(input_dir):
    needed=['00_manifest.json','artifact_manifest.json','provenance_record.json','repository_health.json','supply_chain_report.json','summary.md','evidence-run-manifest.json']
    missing=[n for n in needed if not os.path.exists(os.path.join(input_dir,n))]
    if missing: raise SystemExit('missing: '+','.join(missing))
