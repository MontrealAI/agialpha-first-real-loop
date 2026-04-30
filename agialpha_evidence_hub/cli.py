import argparse, json
from .ingest import load_input
from .validate import validate_manifest, validate_registry, default_manifest
from .registry import register, ensure_structure
from .build import build_site
from .linkcheck import linkcheck
from .discover import discover_to_file
from .backfill import backfill

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('discover'); p.add_argument('--repo-root',default='.'); p.add_argument('--out',default='evidence_registry/discovered.json')
    p=sp.add_parser('register-run'); p.add_argument('--input'); p.add_argument('--registry',default='evidence_registry')
    p=sp.add_parser('build'); p.add_argument('--registry',default='evidence_registry'); p.add_argument('--out',default='_site')
    p=sp.add_parser('validate'); p.add_argument('--site',required=True); p.add_argument('--registry',required=True)
    p=sp.add_parser('linkcheck'); p.add_argument('--site',required=True)
    p=sp.add_parser('backfill'); p.add_argument('--repo-root',default='.'); p.add_argument('--registry',default='evidence_registry')
    p=sp.add_parser('emit-manifest'); p.add_argument('--experiment-slug',required=True); p.add_argument('--out',required=True)
    a=ap.parse_args()
    if a.cmd=='discover': discover_to_file(a.repo_root,a.out)
    elif a.cmd=='register-run': m=load_input(a.input); validate_manifest(m); register(m,a.registry)
    elif a.cmd=='build': build_site(a.registry,a.out)
    elif a.cmd=='validate': validate_registry(a.registry); linkcheck(a.site)
    elif a.cmd=='linkcheck': linkcheck(a.site)
    elif a.cmd=='backfill': ensure_structure(a.registry); backfill(a.repo_root,a.registry)
    elif a.cmd=='emit-manifest':
        m=default_manifest(a.experiment_slug); m['source']='manifest'; m['status']='pending'
        open(a.out,'w').write(json.dumps(m,indent=2))
if __name__=='__main__': main()
