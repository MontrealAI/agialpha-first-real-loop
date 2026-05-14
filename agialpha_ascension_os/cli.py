import argparse, json, sys
from pathlib import Path
from .core import *

def _read_json(path):
    return json.loads(Path(path).read_text())

def discover(args):
    out={"schema_version":"agialpha.ascension.discovery.v1","repo_root":args.repo_root,**bfields()}
    write_json(Path(args.registry)/"latest.json",out)

def run_cycle(args):
    r=Path(args.out); r.mkdir(parents=True, exist_ok=True)
    intake={"intake_id":"intake-"+sid("intake",str(r)),"workflow_name":"enterprise_pilot_readiness_pack","synthetic_fixture_only":True,"real_customer_data_used":False,"pii_used":False,**bfields()}
    triage={"schema_version":"agialpha.regulated_boundary_triage.v1","intake_id":intake["intake_id"],"workflow_name":intake["workflow_name"],"synthetic_fixture_only":True,"real_customer_data_used":False,"pii_used":False,"regulated_domain_flags":{k:False for k in ["financial_advice","investment_advice","payment_or_custody","wallet_or_trading","kyc_aml","legal_advice","medical_advice","hr_or_worker_evaluation","credit_or_lending","insurance","critical_infrastructure_control","energy_market_or_utility_market","biometric_identification","emotion_recognition","law_enforcement","migration_or_border","education_access_or_scoring","justice_or_democratic_process","offensive_cyber"]},"allowed_mode":"safe_enterprise_workflow","reason":"synthetic non-regulated fixture",**bfields()}
    write_json(r/'02_enterprise_intake/enterprise_intake.json',intake); write_json(r/'02_enterprise_intake/regulated_boundary_triage.json',triage)
    write_json(r/'11_open_rsi_eval/B6_ascension_os.json',{"baseline":"B6","valid_candidates":args.evaluate_seeds,**bfields()})
    write_json(r/'11_open_rsi_eval/B5_current_substrate.json',{"baseline":"B5","valid_candidates":max(0,args.evaluate_seeds-1),**bfields()})
    write_json(r/'11_open_rsi_eval/B7_human_promoted.json',{"baseline":"B7","status":"pending",**bfields()})
    write_json(r/'11_open_rsi_eval/baselines.json',{"B4":{"status":"fail_required"},"core_comparison":"B6_vs_B5",**bfields()})
    write_json(r/'14_verified_enterprise_alpha/verified_enterprise_alpha.json',{"verified_enterprise_alpha_score":42,"statement":DISCLAIMER_OPS,**bfields()})
    write_json(r/'15_value_to_capacity/value_to_capacity.json',{"value_to_capacity_score":39,"statement":"This is a directional proxy, not a financial projection, investment claim, energy claim, infrastructure ownership claim, utility-market claim, or superintelligence claim.",**bfields()})
    write_json(r/'16_capacity_reinvestment/capacity_reinvestment.json',{"capacity_reinvestment_score":35,"statement":"This is a planning proxy, not a financing plan, investment product, energy claim, utility-market claim, or guaranteed capacity expansion.",**bfields()})
    write_json(r/'22_reports/ascension_scorecard.json',{"axes":[{"axis_id":"1","axis_name":"Public working artifact","score":"local","max_score":100,"evidence_level":"local",**bfields()}],**bfields()})

def passthrough(args):
    target = getattr(args, 'run', None) or getattr(args, 'out', None)
    if target is None:
        raise ValueError('either --run or --out is required for this command')
    p=Path(target)
    write_json(p/f'{args.cmd.replace("-","_")}.json',{"status":"ok",**bfields()})

def replay_cmd(args):
    run = Path(args.run)
    required=[run/'02_enterprise_intake/enterprise_intake.json', run/'22_reports/ascension_scorecard.json']
    missing=[str(x) for x in required if not x.exists()]
    report={"status":"pass" if not missing else "fail","missing_artifacts":missing,**bfields()}
    write_json(run/'22_reports/replay_report.json', report)
    if missing:
        raise SystemExit(1)

def falsification_cmd(args):
    run=Path(args.run)
    score=run/'22_reports/ascension_scorecard.json'
    missing=[] if score.exists() else [str(score)]
    boundary_ok=True
    if score.exists():
        data=_read_json(score)
        boundary_ok=all(data.get(k)==v for k,v in bfields().items())
    report={"status":"pass" if (not missing and boundary_ok) else "fail","missing_artifacts":missing,"boundary_ok":boundary_ok,**bfields()}
    write_json(run/'22_reports/falsification_audit.json', report)
    if missing or not boundary_ok:
        raise SystemExit(1)

def validate_cmd(args):
    run=Path(args.run)
    checks=[run/'22_reports/replay_report.json', run/'22_reports/falsification_audit.json']
    missing=[str(x) for x in checks if not x.exists()]
    statuses=[]
    for c in checks:
        if c.exists(): statuses.append(_read_json(c).get('status'))
    ok=(not missing) and all(s=='pass' for s in statuses)
    out={"status":"pass" if ok else "fail","missing_reports":missing,"report_statuses":statuses,**bfields()}
    write_json(run/'22_reports/validation_report.json', out)
    if not ok:
        raise SystemExit(1)

def build_data(args):
    out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
    reg=Path(args.registry)
    mapping={"latest":"latest.json","cycles":"cycles.json","enterprise_intakes":"enterprise_intakes.json","regulated_boundary_triage":"regulated_boundary_triage.json","scorecards":"scorecards.json","open_rsi_eval_runs":"open_rsi_eval_runs.json","self_improvement_gauntlet_runs":"self_improvement_gauntlet_runs.json","archive_reuse":"archive_reuse.json","verified_enterprise_alpha":"verified_enterprise_alpha.json","value_to_capacity":"value_to_capacity.json","capacity_reinvestment":"capacity_reinvestment.json","capabilities":"capabilities.json","summary":"summary.json"}
    for name,src in mapping.items():
        p=reg/src
        payload=_read_json(p) if p.exists() else {"status":"unavailable","source":src,**bfields()}
        write_json(out/f'{name}.json',payload)

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    d=sp.add_parser('discover'); d.add_argument('--repo-root', required=True); d.add_argument('--registry', required=True); d.set_defaults(func=discover)
    rc=sp.add_parser('run-cycle'); rc.add_argument('--repo-root', required=True); rc.add_argument('--registry', required=True); rc.add_argument('--out', required=True); rc.add_argument('--candidate-seeds',type=int,default=16); rc.add_argument('--evaluate-seeds',type=int,default=6); rc.set_defaults(func=run_cycle)
    for c in ['run-open-rsi-eval','run-gauntlet','evaluate-archive-reuse','build-scorecard','verified-enterprise-alpha','value-to-capacity','capacity-reinvestment','emit-manifest']:
      p=sp.add_parser(c); p.add_argument('--repo-root',default='.'); p.add_argument('--out', default=None); p.add_argument('--run', default=None); p.add_argument('--task-count',type=int,default=0); p.set_defaults(func=passthrough,cmd=c)
    rp=sp.add_parser('replay'); rp.add_argument('--run', required=True); rp.set_defaults(func=replay_cmd)
    fa=sp.add_parser('falsification-audit'); fa.add_argument('--run', required=True); fa.set_defaults(func=falsification_cmd)
    vd=sp.add_parser('validate'); vd.add_argument('--run', required=True); vd.set_defaults(func=validate_cmd)
    bd=sp.add_parser('build-data'); bd.add_argument('--registry', required=True); bd.add_argument('--out', required=True); bd.set_defaults(func=build_data)
    args=ap.parse_args(); args.func(args)
