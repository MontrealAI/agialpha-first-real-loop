import argparse, json
from .ingest import load_input
from .validate import validate_manifest
from .registry import register
from .build import build_site
from .linkcheck import linkcheck

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    r=sp.add_parser('register-run'); r.add_argument('--input'); r.add_argument('--registry',default='evidence_registry/registry')
    b=sp.add_parser('build'); b.add_argument('--registry',default='evidence_registry/registry'); b.add_argument('--out',default='_site')
    v=sp.add_parser('validate'); v.add_argument('--site'); v.add_argument('--registry')
    l=sp.add_parser('linkcheck'); l.add_argument('--site')
    sp.add_parser('discover'); bf=sp.add_parser('backfill'); bf.add_argument('--repo-root'); bf.add_argument('--out',default='evidence_registry/registry')
    a=ap.parse_args()
    if a.cmd=='register-run': m=load_input(a.input); validate_manifest(m); register(m,a.registry)
    elif a.cmd=='build': build_site(a.registry,a.out)
    elif a.cmd=='validate': linkcheck(a.site)
    elif a.cmd=='linkcheck': linkcheck(a.site)
    elif a.cmd=='discover': print(json.dumps({'ok':True}))
    elif a.cmd=='backfill': print(json.dumps({'ok':True}))
if __name__=='__main__': main()
