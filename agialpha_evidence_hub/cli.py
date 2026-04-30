import argparse
from .discover import discover, backfill
from .ingest import register_run
from .build import build_site
from .validate import validate_site
from .linkcheck import linkcheck

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    sp.add_parser('discover')
    rr=sp.add_parser('register-run'); rr.add_argument('--input',required=True); rr.add_argument('--registry',default='evidence_registry/registry')
    b=sp.add_parser('build'); b.add_argument('--registry',required=True); b.add_argument('--out',required=True)
    v=sp.add_parser('validate'); v.add_argument('--site',required=True); v.add_argument('--registry',required=False)
    l=sp.add_parser('linkcheck'); l.add_argument('--site',required=True)
    bf=sp.add_parser('backfill'); bf.add_argument('--repo-root',default='.'); bf.add_argument('--out',required=True)
    a=p.parse_args()
    if a.cmd=='discover': print(discover())
    elif a.cmd=='register-run': register_run(a.input,a.registry)
    elif a.cmd=='build': build_site(a.registry,a.out)
    elif a.cmd=='validate': validate_site(a.site)
    elif a.cmd=='linkcheck': linkcheck(a.site)
    elif a.cmd=='backfill': backfill(a.repo_root,a.out)

if __name__=='__main__': main()
