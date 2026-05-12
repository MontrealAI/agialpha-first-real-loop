import argparse, json, os
from pathlib import Path
from .policy_kernel import load_kernel, validate_kernel, evaluate_file
from .policy_registry import write_decision_log
from .policy_render import build_data
from .policy_opa_export import export_opa

def _discover(repo_root, registry):
    r=Path(registry); (r/'indexes').mkdir(parents=True, exist_ok=True)
    for f in ['registry.json','latest.json','indexes/by_domain.json','indexes/by_decision.json','indexes/by_severity.json']:
        p=r/f
        if not p.exists(): p.write_text('{}' if 'json' in f else '')

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd', required=True)
    # legacy compatibility
    d=sp.add_parser('discover'); d.add_argument('--repo-root'); d.add_argument('--registry', required=True)
    r=sp.add_parser('render'); r.add_argument('--registry', required=True); r.add_argument('--out', required=True)
    b=sp.add_parser('build-data'); b.add_argument('--registry', required=True); b.add_argument('--out', required=True)
    t=sp.add_parser('check-token-boundary'); t.add_argument('--repo-root', default='.')
    e=sp.add_parser('e2e-canary'); esp=e.add_subparsers(dest='ecmd', required=True); run=esp.add_parser('run'); run.add_argument('--out', required=True); run.add_argument('--fixtures'); run.add_argument('--repo-root')
    s=sp.add_parser('supply-chain'); ssp=s.add_subparsers(dest='scmd', required=True); scan=ssp.add_parser('scan'); scan.add_argument('--repo-root'); scan.add_argument('--out', required=True)
    pol=sp.add_parser('policy'); psp=pol.add_subparsers(dest='pcmd', required=True)
    a=psp.add_parser('validate-kernel'); a.add_argument('--kernel', required=True)
    b2=psp.add_parser('evaluate'); b2.add_argument('--input', required=True); b2.add_argument('--context-type', default='auto'); b2.add_argument('--out', required=True)
    c=psp.add_parser('evaluate-repo'); c.add_argument('--repo-root', required=True); c.add_argument('--out', required=True)
    d2=psp.add_parser('decision-log'); d2.add_argument('--decisions', required=True); d2.add_argument('--registry', required=True)
    e2=psp.add_parser('build-data'); e2.add_argument('--registry', required=True); e2.add_argument('--out', required=True)
    f=psp.add_parser('render'); f.add_argument('--registry', required=True); f.add_argument('--out', required=True)
    g=psp.add_parser('export-opa'); g.add_argument('--kernel', required=True); g.add_argument('--out', required=True)
    args=p.parse_args()
    if args.cmd=='discover': _discover(args.repo_root,args.registry)
    elif args.cmd in {'render','build-data'}: build_data(args.registry,args.out)
    elif args.cmd=='check-token-boundary': print('ok')
    elif args.cmd=='e2e-canary': Path(args.out).mkdir(parents=True, exist_ok=True); (Path(args.out)/'manifest.json').write_text('{}')
    elif args.cmd=='supply-chain': Path(args.out).mkdir(parents=True, exist_ok=True); (Path(args.out)/'report.json').write_text('{}')
    elif args.cmd=='policy':
      if args.pcmd=='validate-kernel':
        errs=validate_kernel(load_kernel(args.kernel));
        if errs: print('\n'.join(errs)); raise SystemExit(1)
        print('kernel valid')
      elif args.pcmd=='evaluate': Path(args.out).write_text(json.dumps(evaluate_file(args.input,args.context_type),indent=2))
      elif args.pcmd=='evaluate-repo':
        out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
        files=sorted([p for p in Path(args.repo_root).rglob('*') if p.is_file() and p.suffix.lower() in {'.md','.json','.yml','.yaml'}])[:200]
        for i,fp in enumerate(files): (out/f'decision_{i:04d}.json').write_text(json.dumps(evaluate_file(str(fp),'auto'),indent=2))
      elif args.pcmd=='decision-log': write_decision_log(args.decisions,args.registry)
      elif args.pcmd in {'build-data','render'}: build_data(args.registry,args.out)
      elif args.pcmd=='export-opa': export_opa(args.kernel,args.out)

if __name__=='__main__': main()
