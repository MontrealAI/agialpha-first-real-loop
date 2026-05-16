import argparse, json
from pathlib import Path
from . import intake, regulated_boundary, customer_attestation, job_packs, validators, proofbundle, docket, work_vault, settlement_receipt, customer_review, external_replay, commercial_readiness, pilot_outcomes, valuation_support_link, registry, validate

def _j(p,d): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(d,indent=2)+"\n",encoding='utf-8')

def build(repo_root: Path, out: Path, workflow_family: str, customer_mode: str):
    pilot_id=f"pilot-{workflow_family}"
    tri=regulated_boundary.triage("synthetic enterprise workflow evidence generation")
    records={}
    records['intake']=intake.make_intake(pilot_id, workflow_family, customer_mode)
    records['triage']=tri
    records['attestation']=customer_attestation.build_attestation(pilot_id)
    records['job_pack']=job_packs.build_job_pack(pilot_id, workflow_family, customer_mode, tri['regulated_boundary_result'])
    records['validator_plan']=validators.build_validator_plan(pilot_id, tri['regulated_boundary_blocked'])
    records['proofbundle']=proofbundle.build_proofbundle(pilot_id, records['validator_plan'])
    records['docket']=docket.build_docket(pilot_id, records['proofbundle']['proofbundle_id'])
    records['work_vault']=work_vault.build_work_vault(pilot_id, records['job_pack']['job_pack_id'])
    records['receipt']=settlement_receipt.build_receipt(pilot_id, records['work_vault']['work_vault_id'])
    records['customer_review']=customer_review.build_customer_review(pilot_id)
    records['external_replay']=external_replay.build_external_replay(pilot_id)
    records['readiness']=commercial_readiness.score(records)
    records['valuation_link']=valuation_support_link.build_link(pilot_id, records['readiness'])
    out.mkdir(parents=True, exist_ok=True)
    _j(out/'01_pilot_intake.json', records['intake']); _j(out/'02_regulated_boundary_triage.json', records['triage']); _j(out/'03_customer_use_attestation.json', records['attestation'])
    _j(out/'04_enterprise_job_pack.json', records['job_pack']); _j(out/'05_validator_plan.json', records['validator_plan']); _j(out/'06_proofbundle.json', records['proofbundle'])
    (out/'07_evidence_docket').mkdir(exist_ok=True); _j(out/'07_evidence_docket'/'docket.json', records['docket'])
    _j(out/'08_work_vault.json', records['work_vault']); _j(out/'09_utility_settlement_receipt.json', records['receipt']); _j(out/'10_customer_review_record.json', records['customer_review'])
    _j(out/'11_external_replay_packet.json', records['external_replay']); _j(out/'12_commercial_readiness_scorecard.json', records['readiness'])
    (out/'13_pilot_outcome_dossier.md').write_text(pilot_outcomes.render_outcome(pilot_id, records['readiness']), encoding='utf-8')
    _j(out/'14_valuation_support_link.json', records['valuation_link']); _j(out/'15_missing_evidence.json', {"missing_evidence": records['readiness']['missing_evidence']})
    _j(out/'00_manifest.json', {"pilot_id":pilot_id}); _j(out/'evidence-run-manifest.json', {"pilot_id":pilot_id});
    (out/'summary.md').write_text('Enterprise pilot summary\n', encoding='utf-8')
    reg=Path('enterprise_pilot_registry'); registry.ensure_registry(reg); run=reg/'runs'/out.name
    if run.exists():
      pass
    else:
      import shutil; shutil.copytree(out, run)
    registry.append_json(reg/'pilots.json', {"pilot_id":pilot_id})
    (reg/'latest.json').write_text(json.dumps({"run_id":out.name},indent=2)+"\n", encoding='utf-8')

def build_data(registry_path: Path, out: Path):
    registry.ensure_registry(registry_path); out.mkdir(parents=True, exist_ok=True)
    mapping={"latest.json":"latest.json","summary.json":"registry.json","pilots.json":"pilots.json","commercial_readiness_scorecards.json":"commercial_readiness_scorecards.json","customer_reviews.json":"customer_reviews.json","external_replay_packets.json":"external_replay_packets.json","valuation_support_links.json":"valuation_support_links.json","missing_evidence.json":"missing_evidence.json"}
    for o,i in mapping.items(): (out/o).write_text((registry_path/i).read_text(encoding='utf-8'), encoding='utf-8')

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd', required=True)
    b=sp.add_parser('build'); b.add_argument('--repo-root', required=True); b.add_argument('--out', required=True); b.add_argument('--workflow-family', required=True); b.add_argument('--customer-mode', required=True); b.set_defaults(func=lambda a: build(Path(a.repo_root), Path(a.out), a.workflow_family, a.customer_mode))
    v=sp.add_parser('validate'); v.add_argument('--run', required=True); v.set_defaults(func=lambda a: validate.validate_run(Path(a.run)))
    d=sp.add_parser('build-data'); d.add_argument('--registry', required=True); d.add_argument('--out', required=True); d.set_defaults(func=lambda a: build_data(Path(a.registry), Path(a.out)))
    s=sp.add_parser('summarize'); s.add_argument('--run', required=True); s.add_argument('--out', required=True); s.set_defaults(func=lambda a: Path(a.out).write_text(pilot_outcomes.render_outcome('pilot', json.loads((Path(a.run)/'12_commercial_readiness_scorecard.json').read_text())), encoding='utf-8'))
    a=p.parse_args(); a.func(a)
