import argparse, json, subprocess, sys
from pathlib import Path
from .supply_chain import collect,build_report,render as sc_render,validate
from .artifact_manifest import build_manifest
from .provenance import build_provenance
from .repository_health import build_repository_health
from .registry import build_indexes

def main():
    if len(sys.argv)>1 and sys.argv[1]=='supply-chain':
      p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
      sc=sp.add_parser('supply-chain'); ssp=sc.add_subparsers(dest='sub',required=True)
      c=ssp.add_parser('collect'); c.add_argument('--repo-root',required=True); c.add_argument('--out',required=True)
      h=ssp.add_parser('hash-artifacts'); h.add_argument('--input',required=True); h.add_argument('--out',required=True)
      pr=ssp.add_parser('provenance'); pr.add_argument('--repo-root',required=True); pr.add_argument('--artifact-manifest',required=True); pr.add_argument('--out',required=True)
      rh=ssp.add_parser('repository-health'); rh.add_argument('--repo-root',required=True); rh.add_argument('--out',required=True)
      br=ssp.add_parser('build-report'); br.add_argument('--input',required=True); br.add_argument('--out',required=True)
      r=ssp.add_parser('render'); r.add_argument('--input',required=True); r.add_argument('--out',required=True)
      v=ssp.add_parser('validate'); v.add_argument('--input',required=True)
      a=p.parse_args();
      {'collect':lambda:collect(a.repo_root,a.out),'hash-artifacts':lambda:build_manifest('.',a.input),'provenance':lambda:build_provenance(a.repo_root,a.artifact_manifest,a.out),'repository-health':lambda:build_repository_health(a.repo_root,a.out),'build-report':lambda:build_report(a.input,a.out),'render':lambda:sc_render(a.input,a.out),'validate':lambda:validate(a.input)}[a.sub]()
      return
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    d=sp.add_parser('discover'); d.add_argument('--repo-root',required=True); d.add_argument('--registry',required=True)
    bd=sp.add_parser('build-data'); bd.add_argument('--registry',required=True); bd.add_argument('--out',required=True)
    r=sp.add_parser('render'); r.add_argument('--registry',required=True); r.add_argument('--out',required=True)
    vr=sp.add_parser('validate-registry'); vr.add_argument('--registry',required=True)
    ctb=sp.add_parser('check-token-boundary'); ctb.add_argument('--repo-root',required=True)
    a=p.parse_args()
    if a.cmd=='discover': build_indexes(a.registry)
    if a.cmd=='build-data':
        reg=Path(a.registry); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
        for n in ['work_vaults','mark_allocations','sovereigns','settlements']:
            arr=[json.loads(p.read_text()) for p in (reg/n).glob('*.json')] if (reg/n).exists() else []
            (out/f'{n}.json').write_text(json.dumps(arr,indent=2))
        s={'work_vault_count':len(json.loads((out/'work_vaults.json').read_text())),'claim_boundary':'SecureRails governance artifact only.'}
        (out/'summary.json').write_text(json.dumps(s,indent=2))
    if a.cmd=='render':
        out=Path(a.out); data=out/'_data'; data.mkdir(parents=True,exist_ok=True)
        subprocess.check_call([sys.executable,'-m','secure_rails','build-data','--registry',a.registry,'--out',str(data)])
        (out/'index.html').write_text('<h1>SecureRails Work Vaults</h1><p>claim boundary applies</p>')
    if a.cmd=='validate-registry':
        r=Path(a.registry); assert (r/'indexes').exists();
    if a.cmd=='check-token-boundary':
        subprocess.check_call([sys.executable,'scripts/secure_rails_claim_boundary_check.py',a.repo_root])
