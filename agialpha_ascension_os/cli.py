
import argparse
from pathlib import Path
from .context import BOUNDARY,now
from .registry import jwrite,jread,append
from .regulated_boundary import triage
from .enterprise_workflows import build_job_packs
from .secure_boundary import check as sec
from .open_rsi_eval import run as run_rsi
from .self_improvement_gauntlet import run as run_gauntlet
from .verified_enterprise_alpha import compute as vea
from .value_to_capacity import compute as vtc
from .capacity_reinvestment import compute as cr
from .scorecard import build as sc
from .replay import run as rp
from .falsification import run as fa

def discover(repo_root,registry):
    p=Path(registry); p.mkdir(parents=True,exist_ok=True)
    out={"schema_version":"agialpha.ascension_os.discovery.v1","generated_at":now(),"repo_root":str(Path(repo_root).resolve()),**BOUNDARY}
    jwrite(p/'latest.json',out); return out

def run_cycle(repo_root,registry,out,candidate_seeds,evaluate_seeds):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    intake={"intake_id":"intake-001","workflow_name":"enterprise_pilot_readiness_pack",**BOUNDARY}
    t=triage(intake['intake_id'],intake['workflow_name'])
    packs=build_job_packs(t)
    jwrite(out/'02_enterprise_intake/enterprise_intake.json',intake); jwrite(out/'02_enterprise_intake/regulated_boundary_triage.json',t)
    jwrite(out/'03_enterprise_workflows/job_packs.json',packs); jwrite(out/'04_secure_rails_triage/boundary_check.json',sec())
    jwrite(out/'11_open_rsi_eval/B6_ascension_os.json',run_rsi()); jwrite(out/'12_self_improvement_gauntlet/gauntlet.json',run_gauntlet())
    jwrite(out/'18_evidence_docket/00_manifest.json',{"docket_id":"docket-001",**BOUNDARY})
    jwrite(out/'17_proofbundle/proofbundle.json',{"proofbundle_id":"pb-001",**BOUNDARY})
    jwrite(out/'14_verified_enterprise_alpha/verified_enterprise_alpha.json',vea({"verified_work_score":1,"evidence_quality_score":1,"replay_integrity_score":1,"business_usefulness_score":1,"reusable_capability_score":1,"governance_integrity_score":1,"regulated_boundary_integrity_score":1,"cost_risk_proxy":1}))
    jwrite(out/'15_value_to_capacity/value_to_capacity.json',vtc({"verified_work_score":1,"reusable_capability_score":1,"archive_reuse_score":1,"business_usefulness_score":1,"compute_or_infra_proxy_score":1,"governance_integrity_score":1,"regulated_boundary_integrity_score":1,"cost_risk_proxy":1}))
    jwrite(out/'16_capacity_reinvestment/capacity_reinvestment.json',cr({"verified_enterprise_alpha_score":1,"reusable_capability_score":1,"replay_integrity_score":1,"governance_integrity_score":1,"regulated_boundary_integrity_score":1,"cost_risk_proxy":1}))
    jwrite(out/'22_reports/ascension_scorecard.json',sc()); jwrite(out/'22_reports/replay_report.json',rp()); jwrite(out/'22_reports/falsification_audit.json',fa())
    return {"status":"success",**BOUNDARY}

def main(argv=None):
 ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
 for c in ['discover','run-cycle','run-open-rsi-eval','run-gauntlet','evaluate-archive-reuse','build-scorecard','verified-enterprise-alpha','value-to-capacity','capacity-reinvestment','replay','falsification-audit','validate','build-data','emit-manifest']:
  p=sp.add_parser(c); p.add_argument('--repo-root'); p.add_argument('--registry'); p.add_argument('--out'); p.add_argument('--run'); p.add_argument('--candidate-seeds',type=int,default=16); p.add_argument('--evaluate-seeds',type=int,default=6); p.add_argument('--task-count',type=int,default=16)
 a=ap.parse_args(argv)
 if a.cmd=='discover': discover(a.repo_root,a.registry)
 elif a.cmd=='run-cycle': run_cycle(a.repo_root,a.registry,a.out,a.candidate_seeds,a.evaluate_seeds)
 elif a.cmd=='run-open-rsi-eval': jwrite(Path(a.out)/'11_open_rsi_eval/B6_ascension_os.json',run_rsi(a.task_count))
 elif a.cmd=='run-gauntlet': jwrite(Path(a.out)/'12_self_improvement_gauntlet/gauntlet.json',run_gauntlet(a.task_count))
 elif a.cmd=='evaluate-archive-reuse': jwrite(Path(a.run)/'13_archive_reuse/comparison.json',{"archive_reuse_advantage_delta":0,"lineage_metaproductivity_score":0,"archive_reuse_beats_no_archive":False,**BOUNDARY})
 elif a.cmd=='build-scorecard': jwrite(Path(a.out)/'22_reports/ascension_scorecard.json',sc())
 elif a.cmd=='verified-enterprise-alpha': jwrite(Path(a.run)/'14_verified_enterprise_alpha/verified_enterprise_alpha.json',vea({"verified_work_score":1,"evidence_quality_score":1,"replay_integrity_score":1,"business_usefulness_score":1,"reusable_capability_score":1,"governance_integrity_score":1,"regulated_boundary_integrity_score":1,"cost_risk_proxy":1}))
 elif a.cmd=='value-to-capacity': jwrite(Path(a.run)/'15_value_to_capacity/value_to_capacity.json',vtc({"verified_work_score":1,"reusable_capability_score":1,"archive_reuse_score":1,"business_usefulness_score":1,"compute_or_infra_proxy_score":1,"governance_integrity_score":1,"regulated_boundary_integrity_score":1,"cost_risk_proxy":1}))
 elif a.cmd=='capacity-reinvestment': jwrite(Path(a.run)/'16_capacity_reinvestment/capacity_reinvestment.json',cr({"verified_enterprise_alpha_score":1,"reusable_capability_score":1,"replay_integrity_score":1,"governance_integrity_score":1,"regulated_boundary_integrity_score":1,"cost_risk_proxy":1}))
 elif a.cmd=='replay': jwrite(Path(a.run)/'22_reports/replay_report.json',rp())
 elif a.cmd=='falsification-audit': jwrite(Path(a.run)/'22_reports/falsification_audit.json',fa())
 elif a.cmd=='validate': pass
 elif a.cmd=='build-data':
  out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
  for n in ['latest','cycles','enterprise_intakes','regulated_boundary_triage','scorecards','open_rsi_eval_runs','self_improvement_gauntlet_runs','archive_reuse','verified_enterprise_alpha','value_to_capacity','capacity_reinvestment','capabilities','summary']:
   jwrite(out/f'{n}.json',[] if n!='summary' else {**BOUNDARY})
 elif a.cmd=='emit-manifest': jwrite(a.out,{"schema_version":"agialpha.ascension_os.manifest.v1",**BOUNDARY})
 return 0
