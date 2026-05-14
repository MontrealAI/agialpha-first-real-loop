
import argparse, datetime
from pathlib import Path
from .registry import jwrite,jread
from .claims import CLAIM_BOUNDARY_FULL, CLAIM_BOUNDARY_SHORT, TOKEN_BOUNDARY
from .scorecard import build_scorecard
from .open_rsi_eval import run_eval
from .archive_reuse_eval import evaluate_archive_reuse
from .value_to_capacity import compute_proxy, DISCLAIMER
from .proofbundle import build_proofbundle
from .docket import build_docket
from .replay import replay_report
from .falsification import falsification_audit

def main(argv=None):
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    for c in ['build-scorecard','run-open-rsi-eval','evaluate-archive-reuse','value-to-capacity','replay','falsification-audit','validate']:
        p=sp.add_parser(c); p.add_argument('--repo-root'); p.add_argument('--out'); p.add_argument('--run'); p.add_argument('--task-count',type=int,default=16)
    bd=sp.add_parser('build-data'); bd.add_argument('--registry',required=True); bd.add_argument('--out',required=True)
    em=sp.add_parser('emit-manifest'); em.add_argument('--run',required=True); em.add_argument('--out',required=True)
    a=ap.parse_args(argv)
    run=Path(getattr(a,'run',None) or getattr(a,'out',None) or '.')
    if a.cmd=='build-scorecard':
        jwrite(run/'01_public_evidence_scorecard.json', {**build_scorecard(),"claim_boundary":CLAIM_BOUNDARY_FULL,"token_boundary":TOKEN_BOUNDARY,"human_review_required":True})
    elif a.cmd=='run-open-rsi-eval':
        r=run_eval(a.task_count); jwrite(run/'02_open_rsi_eval/open_rsi_eval.json',r); jwrite(run/'02_open_rsi_eval/baselines.json',r['baselines'])
    elif a.cmd=='evaluate-archive-reuse': jwrite(run/'03_archive_reuse/comparison.json', evaluate_archive_reuse())
    elif a.cmd=='value-to-capacity':
        v=compute_proxy(); jwrite(run/'04_value_to_capacity/value_to_capacity.json',v); (run/'04_value_to_capacity/value_to_capacity.md').write_text(DISCLAIMER+'\n'); (run/'04_value_to_capacity/value_to_capacity_claim_boundary.md').write_text(DISCLAIMER+'\n')
    elif a.cmd=='replay': jwrite(run/'07_replay/replay_report.json', replay_report())
    elif a.cmd=='falsification-audit': jwrite(run/'08_falsification/falsification_audit.json', falsification_audit())
    elif a.cmd=='validate':
        required=['01_public_evidence_scorecard.json','02_open_rsi_eval/open_rsi_eval.json','03_archive_reuse/comparison.json','04_value_to_capacity/value_to_capacity.json']
        miss=[x for x in required if not (run/x).exists()]
        if miss: raise SystemExit('missing:'+','.join(miss))
    elif a.cmd=='emit-manifest': jwrite(a.out,{"run":str(a.run),"claim_boundary":CLAIM_BOUNDARY_SHORT,"token_boundary":TOKEN_BOUNDARY,"human_review_required":True,"no_autonomous_persistence":True})
    elif a.cmd=='build-data':
        reg=Path(a.registry); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
        sources = {
            'latest': 'latest.json',
            'scorecards': 'scorecards.json',
            'open_rsi_eval_runs': 'open_rsi_eval_runs.json',
            'public_evidence_axes': 'public_evidence_axes.json',
            'archive_reuse': 'archive_reuse_results.json',
            'value_to_capacity': 'value_to_capacity_results.json',
            'summary': 'summary.json',
        }
        for name, source in sources.items():
            default = {} if name == 'summary' else []
            jwrite(out / f'{name}.json', jread(reg / source, default))
    return 0
