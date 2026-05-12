import argparse, json
from pathlib import Path

from .artifact_manifest import build_manifest
from .provenance import build_provenance
from .repository_health import build_repository_health
from .supply_chain import collect, build_report as sc_build_report, render as sc_render, validate as sc_validate
from .token_boundary import check_token_boundary
from .discover import discover
from .registry import build_indexes
from .render import build_data as sr_build_data, render_html
from .github_app_permissions import validate_permission_matrix
from .e2e_canary import validate as canary_validate
from .canary_runner import run_canary
from .canary_replay import replay as canary_replay
from .canary_report import build_report as canary_build_report
from .canary_registry import update_registry as canary_update_registry, build_data as canary_build_data
from .canary_render import render as canary_render
from .policy_kernel import load_kernel, validate_kernel, evaluate_file
from .policy_registry import write_decision_log
from .policy_render import build_data as policy_build_data
from .policy_opa_export import export_opa


def main():
    p = argparse.ArgumentParser(); sp = p.add_subparsers(dest='cmd', required=True)
    d=sp.add_parser('discover'); d.add_argument('--repo-root', required=True); d.add_argument('--registry', required=True)
    vreg=sp.add_parser('validate-registry'); vreg.add_argument('--registry', required=True)
    r=sp.add_parser('render'); r.add_argument('--registry', required=True); r.add_argument('--out', required=True)
    b=sp.add_parser('build-data'); b.add_argument('--registry', required=True); b.add_argument('--out', required=True)
    t=sp.add_parser('check-token-boundary'); t.add_argument('--repo-root', default='.')
    ga=sp.add_parser('github-app'); ga.add_argument('--permissions', required=True)

    e=sp.add_parser('e2e-canary'); esp=e.add_subparsers(dest='ecmd', required=True)
    er=esp.add_parser('run'); er.add_argument('--repo-root', required=True); er.add_argument('--fixtures', required=True); er.add_argument('--out', required=True)
    ep=esp.add_parser('replay'); ep.add_argument('--input', required=True); ep.add_argument('--out', required=True)
    ev=esp.add_parser('validate'); ev.add_argument('--input', required=True)
    ebr=esp.add_parser('build-report'); ebr.add_argument('--input', required=True); ebr.add_argument('--out', required=True)
    erd=esp.add_parser('render'); erd.add_argument('--input', required=True); erd.add_argument('--out', required=True)
    eur=esp.add_parser('update-registry'); eur.add_argument('--input', required=True); eur.add_argument('--registry', required=True)
    ebd=esp.add_parser('build-data'); ebd.add_argument('--registry', required=True); ebd.add_argument('--out', required=True)

    s=sp.add_parser('supply-chain'); ssp=s.add_subparsers(dest='scmd', required=True)
    sc=ssp.add_parser('scan'); sc.add_argument('--repo-root', required=True); sc.add_argument('--out', required=True)
    scol=ssp.add_parser('collect'); scol.add_argument('--repo-root', required=True); scol.add_argument('--out', required=True)
    sha=ssp.add_parser('hash-artifacts'); sha.add_argument('--input', required=True); sha.add_argument('--out', required=True)
    prov=ssp.add_parser('provenance'); prov.add_argument('--repo-root', required=True); prov.add_argument('--artifact-manifest', required=True); prov.add_argument('--out', required=True)
    rh=ssp.add_parser('repository-health'); rh.add_argument('--repo-root', required=True); rh.add_argument('--out', required=True)
    sbr=ssp.add_parser('build-report'); sbr.add_argument('--input', required=True); sbr.add_argument('--out', required=True)
    sren=ssp.add_parser('render'); sren.add_argument('--input', required=True); sren.add_argument('--out', required=True)
    sval=ssp.add_parser('validate'); sval.add_argument('--input', required=True)

    pol=sp.add_parser('policy'); psp=pol.add_subparsers(dest='pcmd', required=True)
    a=psp.add_parser('validate-kernel'); a.add_argument('--kernel', required=True)
    b2=psp.add_parser('evaluate'); b2.add_argument('--input', required=True); b2.add_argument('--context-type', default='auto'); b2.add_argument('--out', required=True)
    c=psp.add_parser('evaluate-repo'); c.add_argument('--repo-root', required=True); c.add_argument('--out', required=True)
    d2=psp.add_parser('decision-log'); d2.add_argument('--decisions', required=True); d2.add_argument('--registry', required=True)
    e2=psp.add_parser('build-data'); e2.add_argument('--registry', required=True); e2.add_argument('--out', required=True)
    f=psp.add_parser('render'); f.add_argument('--registry', required=True); f.add_argument('--out', required=True)
    g=psp.add_parser('export-opa'); g.add_argument('--kernel', required=True); g.add_argument('--out', required=True)

    args = p.parse_args()
    if args.cmd == 'discover':
        discover(Path(args.repo_root), Path(args.registry)); build_indexes(Path(args.registry))
    elif args.cmd == 'validate-registry':
        build_indexes(Path(args.registry))
    elif args.cmd == 'build-data':
        sr_build_data(Path(args.registry), Path(args.out))
    elif args.cmd == 'render':
        render_html(Path(args.registry), Path(args.out))
    elif args.cmd == 'check-token-boundary':
        raise SystemExit(0 if check_token_boundary(Path(args.repo_root)) else 1)
    elif args.cmd == 'github-app':
        ok, _ = validate_permission_matrix(json.loads(Path(args.permissions).read_text()))
        raise SystemExit(0 if ok else 1)
    elif args.cmd == 'e2e-canary':
        if args.ecmd == 'run': run_canary(Path(args.repo_root), Path(args.fixtures), Path(args.out))
        elif args.ecmd == 'replay':
            rep = canary_replay(Path(args.input), Path(args.out)); raise SystemExit(0 if rep.get('replay_pass') else 1)
        elif args.ecmd == 'validate': canary_validate(Path(args.input))
        elif args.ecmd == 'build-report': canary_build_report(Path(args.input), Path(args.out))
        elif args.ecmd == 'render': canary_render(Path(args.input), Path(args.out))
        elif args.ecmd == 'update-registry': canary_update_registry(Path(args.input), Path(args.registry))
        elif args.ecmd == 'build-data': canary_build_data(Path(args.registry), Path(args.out))
    elif args.cmd == 'supply-chain':
        if args.scmd in {'scan','collect'}: collect(args.repo_root, args.out)
        elif args.scmd == 'hash-artifacts':
            m = build_manifest(args.input, str(Path(args.out).parent))
            Path(args.out).write_text(json.dumps(m, indent=2))
        elif args.scmd == 'provenance': build_provenance(args.repo_root, args.artifact_manifest, args.out)
        elif args.scmd == 'repository-health': build_repository_health(args.repo_root, args.out)
        elif args.scmd == 'build-report': sc_build_report(args.input, args.out)
        elif args.scmd == 'render': sc_render(args.input, args.out)
        elif args.scmd == 'validate': sc_validate(args.input)
    elif args.cmd == 'policy':
        if args.pcmd == 'validate-kernel':
            errs = validate_kernel(load_kernel(args.kernel));
            if errs: print('\n'.join(errs)); raise SystemExit(1)
            print('kernel valid')
        elif args.pcmd == 'evaluate': Path(args.out).write_text(json.dumps(evaluate_file(args.input, args.context_type), indent=2))
        elif args.pcmd == 'evaluate-repo':
            out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
            files=sorted([p for p in Path(args.repo_root).rglob('*') if p.is_file() and p.suffix.lower() in {'.md','.json','.yml','.yaml'}])[:200]
            for i,fp in enumerate(files): (out/f'decision_{i:04d}.json').write_text(json.dumps(evaluate_file(str(fp),'auto'),indent=2))
        elif args.pcmd == 'decision-log': write_decision_log(args.decisions, args.registry)
        elif args.pcmd in {'build-data','render'}: policy_build_data(args.registry, args.out)
        elif args.pcmd == 'export-opa': export_opa(args.kernel, args.out)


if __name__ == '__main__':
    main()
