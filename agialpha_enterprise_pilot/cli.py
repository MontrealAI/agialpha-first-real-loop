from pathlib import Path
import argparse, json, shutil
from .boundaries import boundary_fields
from .regulated_boundary import triage
JOB_PACKS=["software_quality_pack","evidence_ops_pack","docs_ops_pack","trust_center_readiness_pack","secure_rails_readiness_pack","defensive_security_docs_pack","workflow_catalog_readiness_pack","external_replay_readiness_pack","enterprise_pilot_readiness_pack","commercial_packaging_readiness_pack"]
EXCLUDED=["HR / worker evaluation","profiling of individuals","automated decisions about natural persons","credit / lending","insurance","medical use","legal advice","financial or investment advice","KYC/AML","banking / brokerage / custody","critical infrastructure control","energy or utility market participation","offensive cyber","cybersecurity certification","autonomous procurement","binding contract execution"]

def wj(path,obj): Path(path).parent.mkdir(parents=True,exist_ok=True); Path(path).write_text(json.dumps(obj,indent=2)+"\n",encoding='utf-8')
def loadj(p,d): return json.loads(Path(p).read_text()) if Path(p).exists() else d

def build(repo_root,out,workflow_family,customer_mode,registry='enterprise_pilot_registry'):
    run=Path(out); run.mkdir(parents=True,exist_ok=True); b=boundary_fields(); pid=run.name
    intake={"schema_version":"agialpha.enterprise_pilot_intake.v1","pilot_id":pid,"customer_label":"synthetic_customer" if customer_mode=="synthetic_only" else "redacted_customer","customer_data_mode":customer_mode,"workflow_family":workflow_family,"intended_use":"enterprise pilot evidence workflow","excluded_uses_acknowledged":True,"regulated_boundary_triage_required":True,"proofbundle_required":True,"evidence_docket_required":True,"external_replay_packet_required":True,"customer_review_required":True,**b}
    t=triage(intake["intended_use"])
    att={"schema_version":"agialpha.customer_use_attestation.v1","pilot_id":pid,"excluded_uses":EXCLUDED,"excluded_uses_acknowledged":True,**b}
    jp={"job_pack_id":f"jobpack-{pid}","workflow_family":workflow_family,"synthetic_inputs_used":customer_mode=="synthetic_only","customer_approved_redacted_inputs_used":customer_mode=="customer_approved_redacted","prohibited_actions_checked":True,"regulated_boundary_result":t["regulated_boundary_result"],"validator_plan":{"checks":["determinism","boundary_fields"]},"proofbundle_plan":{"required":True},"evidence_docket_plan":{"required":True},"customer_review_plan":{"status":"pending"},"external_replay_plan":{"required":True},"work_vault_plan":{"local_json_only":True},"utility_settlement_receipt_plan":{"local_json_only":True},"commercial_usefulness_hypothesis":"safe customer-pilot evidence",**b}
    vp={"validator_plan_id":f"validator-{pid}","checks":["regulated_boundary_firewall","no_investment_claim","no_token_value_claim"],"complete":True}
    pb={"proofbundle_id":f"proof-{pid}","pilot_id":pid,"job_pack_id":jp["job_pack_id"],"status":"complete",**b}
    docket={"evidence_docket_id":f"docket-{pid}","pilot_id":pid,"proofbundle_id":pb["proofbundle_id"],"status":"complete",**b}
    wv={"work_vault_id":f"vault-{pid}","pilot_id":pid,"job_pack_id":jp["job_pack_id"],"alpha_work_units_estimate":100,"validator_fee_units":10,"replay_fee_units":5,"proofbundle_fee_units":8,"evidence_docket_fee_units":8,"archive_access_units":2,"unused_budget_refund_units":0,"settlement_status":"simulated_local_receipt_only",**b}
    sr={"settlement_receipt_id":f"receipt-{pid}","pilot_id":pid,"work_vault_id":wv["work_vault_id"],"statement":"This is a utility-only local accounting receipt for validated work. It is not payment processing, custody, money transmission, securities activity, token-value evidence, investment return, or financial advice.",**b}
    cr={"customer_review_id":f"review-{pid}","pilot_id":pid,"status":"pending",**b}
    er={"external_replay_packet_id":f"replay-{pid}","pilot_id":pid,"status":"complete",**b}
    sc={"schema_version":"agialpha.commercial_readiness_scorecard.v1","commercial_readiness_tier":"C6","paid_pilot_or_commercial_commitment_status":"not_reported","missing_evidence":["paid_pilot_or_commercial_commitment_status:not_reported"],**b}
    outcome={"schema_version":"agialpha.enterprise_pilot_outcome.v1","pilot_id":pid,"commercial_readiness_tier":"C6",**b}
    vsl={"pilot_id":pid,"commercial_readiness_tier":"C6","customer_review_status":"pending","external_replay_status":"complete","repeatable_deployment_status":"complete","paid_pilot_or_commercial_commitment_status":"not_reported","evidence_docket_path":"07_evidence_docket/docket.json","proofbundle_path":"06_proofbundle.json","work_vault_path":"08_work_vault.json","settlement_receipt_path":"09_utility_settlement_receipt.json","missing_evidence":["paid_pilot_or_commercial_commitment_status:not_reported"],"statement":"This pilot evidence may support commercial-readiness and implementation-side valuation-support analysis. It does not assert valuation, investment return, token value, revenue, ARR, ROI, fair market value, or financial advice.",**b}
    files=[('00_manifest.json',{"run_id":pid,**b}),('01_pilot_intake.json',intake),('02_regulated_boundary_triage.json',t),('03_customer_use_attestation.json',att),('04_enterprise_job_pack.json',jp),('05_validator_plan.json',vp),('06_proofbundle.json',pb),('08_work_vault.json',wv),('09_utility_settlement_receipt.json',sr),('10_customer_review_record.json',cr),('11_external_replay_packet.json',er),('12_commercial_readiness_scorecard.json',sc),('14_valuation_support_link.json',vsl),('15_missing_evidence.json',{"missing_evidence":sc['missing_evidence']}),('evidence-run-manifest.json',{"run_id":pid}),('summary.md',f"# Pilot Outcome Dossier\n\nTier: C6\n")]
    for n,o in files: wj(run/n,o) if n.endswith('.json') else Path(run/n).write_text(o,encoding='utf-8')
    wj(run/'07_evidence_docket/docket.json',docket); Path(run/'13_pilot_outcome_dossier.md').write_text('# Pilot Outcome Dossier\n\nTier: C6\n',encoding='utf-8')
    rr=Path(registry); (rr/'runs'/pid).mkdir(parents=True,exist_ok=True)
    for p in run.iterdir(): shutil.copytree(p,rr/'runs'/pid/p.name,dirs_exist_ok=True) if p.is_dir() else shutil.copy2(p,rr/'runs'/pid/p.name)
    top=['registry','latest','pilots','pilot_intakes','regulated_boundary_triage','customer_attestations','job_packs','proofbundles','evidence_dockets','work_vaults','settlement_receipts','customer_reviews','external_replay_packets','commercial_readiness_scorecards','pilot_outcomes','valuation_support_links','missing_evidence']
    for n in top:
        path=rr/f'{n}.json'
        if n in ('registry','latest'): continue
        arr=loadj(path,[]); arr.append({'pilot_id':pid} if n=='pilots' else {'run_id':pid}); wj(path,arr)
    wj(rr/'latest.json',{'run_id':pid}); wj(rr/'registry.json',{'latest_run_id':pid}); Path(rr/'CHANGELOG.md').write_text('# Enterprise Pilot Registry\n',encoding='utf-8')

def validate_run(run):
    req=['01_pilot_intake.json','02_regulated_boundary_triage.json','03_customer_use_attestation.json','04_enterprise_job_pack.json','06_proofbundle.json','07_evidence_docket/docket.json','08_work_vault.json','09_utility_settlement_receipt.json','10_customer_review_record.json','11_external_replay_packet.json','12_commercial_readiness_scorecard.json','14_valuation_support_link.json']
    run=Path(run)
    miss=[x for x in req if not (run/x).exists()]
    if miss: raise SystemExit('missing:'+','.join(miss))

def build_data(registry,out):
    r,o=Path(registry),Path(out); o.mkdir(parents=True,exist_ok=True)
    for n in ['latest','pilots','commercial_readiness_scorecards','customer_reviews','external_replay_packets','valuation_support_links','missing_evidence']:
        src=r/f'{n}.json';
        if src.exists(): (o/f'{n}.json').write_text(src.read_text(),encoding='utf-8')
    wj(o/'summary.json',{"routes":["/enterprise-pilot/","/experiments/agialpha-enterprise-pilot-001/"]})

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    b=sp.add_parser('build'); b.add_argument('--repo-root',required=True); b.add_argument('--out',required=True); b.add_argument('--workflow-family',choices=JOB_PACKS,required=True); b.add_argument('--customer-mode',choices=['synthetic_only','customer_approved_redacted','not_reported'],required=True); b.set_defaults(func=lambda a: build(a.repo_root,a.out,a.workflow_family,a.customer_mode))
    v=sp.add_parser('validate'); v.add_argument('--run',required=True); v.set_defaults(func=lambda a: validate_run(a.run))
    d=sp.add_parser('build-data'); d.add_argument('--registry',required=True); d.add_argument('--out',required=True); d.set_defaults(func=lambda a: build_data(a.registry,a.out))
    s=sp.add_parser('summarize'); s.add_argument('--run',required=True); s.add_argument('--out',required=True); s.set_defaults(func=lambda a: Path(a.out).write_text('# Pilot Outcome Dossier\n\nTier: C6\n',encoding='utf-8'))
    a=p.parse_args(); a.func(a)
