import argparse, json
from pathlib import Path
from .pr_context import load_event, build_context
from .diff_parser import pr_diff_summary
from .workflow_permissions import review_workflows
from .secret_redaction import scan_text
from .claim_boundary import review_claims, BOUNDARY
from .no_automerge import review_no_automerge
from .work_vault import build_work_vault
from .mark import allocate_mark
from .sovereign import assign_sovereign
from .safety_ledger import build_safety_ledger
from .proofbundle import build_proofbundle
from .validator_report import build_validator_report
from .settlement import build_settlement
from .capability_archive import build_candidate
from .evidence_docket import build_evidence
from .render import render_summary

def _write(p,o): Path(p).write_text(json.dumps(o,indent=2))

def analyze(args):
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    ev=load_event(args.event_path); ctx=build_context(args.repo_root,ev)
    texts={}
    for p in Path(args.repo_root).rglob('*'):
        if p.is_file() and '.git' not in p.parts:
            try:texts[str(p.relative_to(args.repo_root))]=p.read_text(errors='ignore')
            except:pass
    diff=pr_diff_summary(args.repo_root); wf=review_workflows(args.repo_root)
    secrets=[f for k,v in texts.items() for f in scan_text(k,v)]
    claims=review_claims(texts); no_auto=review_no_automerge(texts)
    vault=build_work_vault(ctx); mark=allocate_mark(diff,wf,claims,no_auto); sov=assign_sovereign(diff,wf,secrets,claims,no_auto)
    ledger=build_safety_ledger(secrets,no_auto)
    rec='human_review_required'
    if no_auto['findings'] or secrets: rec='reject'
    elif wf['risks'] or claims['violations']: rec='escalate'
    manifest={'schema_version':'securerails.pr_guard_run.v1','experiment_slug':'securerails-agentic-pr-guard-001','run_id':ctx['run_id'],'run_url':ctx['run_url'],'repository':ctx['repository'],'pull_request':ctx['pull_request'],'status':'success','claim_level':'local-pr-guard','work_vault_id':vault['work_vault_id'],'mark_allocation_id':'mark-'+ctx['run_id'],'assigned_sovereign':sov['primary'],'proofbundle_id':'proofbundle-'+ctx['run_id'],'evidence_docket_id':'docket-'+ctx['run_id'],'human_review_required':True,'auto_merge_allowed':False,'safety':ledger,'decision':{'recommendation':rec,'reason':'Automated advisory recommendation only; human review required.'},'claim_boundary':BOUNDARY}
    _write(out/'00_manifest.json',manifest);_write(out/'01_work_vault.json',vault);_write(out/'02_mark_allocation.json',mark);_write(out/'03_sovereign_assignment.json',sov);_write(out/'04_pr_diff_summary.json',diff);_write(out/'05_workflow_permission_review.json',wf);_write(out/'06_redacted_secret_hygiene_report.json',{'findings':secrets,'claim_boundary':BOUNDARY});_write(out/'07_claim_boundary_review.json',claims);_write(out/'08_no_automerge_review.json',no_auto);_write(out/'09_safety_ledger.json',ledger)
    build_proofbundle(out)
    checklist='''- [ ] Review manifest
- [ ] Review safety ledger
- [ ] Confirm claim boundary
- [ ] Decide: remediate/reject/escalate
'''
    (out/'13_human_review_checklist.md').write_text(checklist)
    _write(out/'12_validator_report.json',build_validator_report(rec));_write(out/'14_settlement_record.json',build_settlement(vault['work_vault_id']));_write(out/'15_capability_archive_candidate.json',build_candidate(rec))
    build_evidence(out,out/'11_evidence_docket')
    (out/'evidence-run-manifest.json').write_text(json.dumps({'experiment_slug':'securerails-agentic-pr-guard-001','output_root':str(out),'claim_boundary':BOUNDARY},indent=2))

def validate(args):
    required=['00_manifest.json','01_work_vault.json','02_mark_allocation.json','03_sovereign_assignment.json','09_safety_ledger.json','12_validator_report.json']
    miss=[x for x in required if not (Path(args.input)/x).exists()]
    if miss: raise SystemExit('Missing: '+','.join(miss))

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('analyze'); a.add_argument('--repo-root',required=True); a.add_argument('--event-path'); a.add_argument('--out',required=True); a.set_defaults(func=analyze)
    v=sp.add_parser('validate'); v.add_argument('--input',required=True); v.set_defaults(func=validate)
    r=sp.add_parser('render-summary'); r.add_argument('--input',required=True); r.add_argument('--out',required=True); r.set_defaults(func=lambda x: render_summary(x.input,x.out))
    b=sp.add_parser('build-evidence'); b.add_argument('--input',required=True); b.add_argument('--out',required=True); b.set_defaults(func=lambda x: build_evidence(x.input,x.out))
    args=ap.parse_args(); args.func(args)

if __name__=='__main__': main()
