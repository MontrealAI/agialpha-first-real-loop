import argparse, json, os
from .work_vaults import create_work_vault
from .mark import score_mark
from .sovereigns import assign_sovereign
from .agi_jobs import run_job
from .proofbundles import make_proofbundle
from .evidence_dockets import make_evidence_docket
from .settlement import make_settlement
from .capability_archive import make_archive
from .validators import validate_vault
from .render import render

def _load(p): return json.load(open(p))
def main():
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest='cmd',required=True)
 a=sp.add_parser('create-vault');a.add_argument('--repo-root');a.add_argument('--out',required=True)
 b=sp.add_parser('score-mark');b.add_argument('--vault',required=True)
 c=sp.add_parser('assign-sovereign');c.add_argument('--vault',required=True)
 d=sp.add_parser('run-demo-job');d.add_argument('--vault',required=True)
 e=sp.add_parser('validate-vault');e.add_argument('--vault',required=True)
 f=sp.add_parser('render');f.add_argument('--run',required=True);f.add_argument('--out',required=True)
 args=p.parse_args()
 if args.cmd=='create-vault':
  out=args.out;v=create_work_vault(out);m=score_mark(out,v);assign_sovereign(out);run_job(out,v);make_proofbundle(out,v);make_evidence_docket(out,v);
  json.dump(v['hard_safety_counters'],open(os.path.join(out,'safety-ledger.json'),'w'),indent=2)
  make_settlement(out,v);make_archive(out,v)
  open(os.path.join(out,'README.md'),'w').write('SecureRails deterministic demo artifacts. Utility accounting only.\n')
  manifest={"experiment_slug":"securerails-work-vault-demo","experiment_family":"securerails","claim_level":"local-demo","claim_boundary":v['claim_boundary'],"public_page":"docs/secure-rails/work-vaults-demo/README.md","raw_json_links":sorted(f for f in os.listdir(out) if f.endswith('.json')),"safety_counters":v['hard_safety_counters']}
  json.dump(manifest,open(os.path.join(out,'evidence-run-manifest.json'),'w'),indent=2)
 if args.cmd=='score-mark': score_mark(os.path.dirname(args.vault),_load(args.vault))
 if args.cmd=='assign-sovereign': assign_sovereign(os.path.dirname(args.vault))
 if args.cmd=='run-demo-job': v=_load(args.vault);run_job(os.path.dirname(args.vault),v);make_proofbundle(os.path.dirname(args.vault),v);make_evidence_docket(os.path.dirname(args.vault),v);make_settlement(os.path.dirname(args.vault),v);make_archive(os.path.dirname(args.vault),v)
 if args.cmd=='validate-vault':
  ok=validate_vault(_load(args.vault));print('valid' if ok else 'invalid');raise SystemExit(0 if ok else 1)
 if args.cmd=='render': render(args.run,args.out)
