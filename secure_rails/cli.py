import argparse
import json
from pathlib import Path

from .discover import discover
from .registry import build_indexes
from .render import build_data as build_registry_data, render_html
from .token_boundary import check_token_boundary
from .e2e_canary import run_canary, replay, build_report, update_registry, build_data as canary_build_data, render, validate as canary_validate, list_fixtures_cmd
from .supply_chain import collect as sc_collect, build_report as sc_build_report, render as sc_render, validate as sc_validate

from .policy_kernel import load_kernel, validate_kernel, evaluate_file
from .policy_registry import write_decision_log
from .policy_render import build_data as build_policy_data
from .policy_opa_export import export_opa
from .validate import validate_registry as semantic_validate_registry


def _validate_registry(registry: Path) -> int:
    required = [registry / 'indexes' / 'by_status.json', registry / 'indexes' / 'by_sovereign.json']
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        print('missing:', ', '.join(missing))
        return 1
    if not semantic_validate_registry(registry):
        return 1
    return 0


def main() -> None:
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd', required=True)

    d = sp.add_parser('discover'); d.add_argument('--repo-root', required=True); d.add_argument('--registry', required=True)
    r = sp.add_parser('render'); r.add_argument('--registry', required=True); r.add_argument('--out', required=True)
    b = sp.add_parser('build-data'); b.add_argument('--registry', required=True); b.add_argument('--out', required=True)
    vr = sp.add_parser('validate-registry'); vr.add_argument('--registry', required=True)

    t = sp.add_parser('check-token-boundary'); t.add_argument('--repo-root', default='.')
    cwv = sp.add_parser('check-work-vaults'); cwv.add_argument('--registry', required=True)
    gh = sp.add_parser('github-app'); ghsp = gh.add_subparsers(dest='gcmd', required=True); ghsp.add_parser('validate')

    e = sp.add_parser('e2e-canary'); esp = e.add_subparsers(dest='ecmd', required=True)
    e_run = esp.add_parser('run'); e_run.add_argument('--repo-root', required=True); e_run.add_argument('--fixtures', required=True); e_run.add_argument('--out', required=True)
    e_replay = esp.add_parser('replay'); e_replay.add_argument('--input', required=True); e_replay.add_argument('--out', required=True)
    e_validate = esp.add_parser('validate'); e_validate.add_argument('--input', required=True)
    e_report = esp.add_parser('build-report'); e_report.add_argument('--input', required=True); e_report.add_argument('--out', required=True)
    e_reg = esp.add_parser('update-registry'); e_reg.add_argument('--input', required=True); e_reg.add_argument('--registry', required=True)
    e_data = esp.add_parser('build-data'); e_data.add_argument('--registry', required=True); e_data.add_argument('--out', required=True)
    e_render = esp.add_parser('render'); e_render.add_argument('--input', required=True); e_render.add_argument('--out', required=True)
    e_list = esp.add_parser('list-fixtures'); e_list.add_argument('--fixtures', required=True)

    s = sp.add_parser('supply-chain'); ssp = s.add_subparsers(dest='scmd', required=True)
    s_collect = ssp.add_parser('collect'); s_collect.add_argument('--repo-root', required=True); s_collect.add_argument('--out', required=True)
    s_hash = ssp.add_parser('hash-artifacts'); s_hash.add_argument('--input', required=True); s_hash.add_argument('--out', required=True)
    s_prov = ssp.add_parser('provenance'); s_prov.add_argument('--repo-root', required=True); s_prov.add_argument('--artifact-manifest', required=True); s_prov.add_argument('--out', required=True)
    s_health = ssp.add_parser('repository-health'); s_health.add_argument('--repo-root', required=True); s_health.add_argument('--out', required=True)
    s_brep = ssp.add_parser('build-report'); s_brep.add_argument('--input', required=True); s_brep.add_argument('--out', required=True)
    s_rend = ssp.add_parser('render'); s_rend.add_argument('--input', required=True); s_rend.add_argument('--out', required=True)
    s_val = ssp.add_parser('validate'); s_val.add_argument('--input', required=True)

    pol = sp.add_parser('policy'); psp = pol.add_subparsers(dest='pcmd', required=True)
    a = psp.add_parser('validate-kernel'); a.add_argument('--kernel', required=True)
    b2 = psp.add_parser('evaluate'); b2.add_argument('--input', required=True); b2.add_argument('--context-type', default='auto'); b2.add_argument('--out', required=True)
    c = psp.add_parser('evaluate-repo'); c.add_argument('--repo-root', required=True); c.add_argument('--out', required=True)
    d2 = psp.add_parser('decision-log'); d2.add_argument('--decisions', required=True); d2.add_argument('--registry', required=True)
    e2 = psp.add_parser('build-data'); e2.add_argument('--registry', required=True); e2.add_argument('--out', required=True)
    f = psp.add_parser('render'); f.add_argument('--registry', required=True); f.add_argument('--out', required=True)
    g = psp.add_parser('export-opa'); g.add_argument('--kernel', required=True); g.add_argument('--out', required=True)

    args = p.parse_args()
    if args.cmd == 'discover':
        discover(Path(args.repo_root), Path(args.registry)); build_indexes(Path(args.registry))
    elif args.cmd == 'build-data':
        build_registry_data(Path(args.registry), Path(args.out))
    elif args.cmd == 'render':
        render_html(Path(args.registry), Path(args.out))
    elif args.cmd == 'validate-registry':
        raise SystemExit(_validate_registry(Path(args.registry)))
    elif args.cmd == 'check-token-boundary':
        raise SystemExit(0 if check_token_boundary(Path(args.repo_root)) else 1)
    elif args.cmd == 'check-work-vaults':
        reg = Path(args.registry)
        build_indexes(reg)
        raise SystemExit(0 if semantic_validate_registry(reg) else 1)
    elif args.cmd == 'github-app':
        print('github-app command validated')
    elif args.cmd == 'e2e-canary':
        if args.ecmd == 'run': run_canary(Path(args.repo_root), Path(args.fixtures), Path(args.out))
        elif args.ecmd == 'replay':
            rep = replay(Path(args.input), Path(args.out))
            if not rep.get('replay_pass', False):
                raise SystemExit(1)
        elif args.ecmd == 'validate': canary_validate(Path(args.input))
        elif args.ecmd == 'build-report': build_report(Path(args.input), Path(args.out))
        elif args.ecmd == 'update-registry': update_registry(Path(args.input), Path(args.registry))
        elif args.ecmd == 'build-data': canary_build_data(Path(args.registry), Path(args.out))
        elif args.ecmd == 'render': render(Path(args.input), Path(args.out))
        elif args.ecmd == 'list-fixtures': list_fixtures_cmd(Path(args.fixtures))
    elif args.cmd == 'supply-chain':
        if args.scmd == 'collect': sc_collect(args.repo_root, args.out)
        elif args.scmd == 'hash-artifacts':
            from .artifact_manifest import build_manifest
            out_path = Path(args.out)
            manifest = build_manifest(args.input, str(out_path.parent))
            out_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        elif args.scmd == 'provenance':
            from .provenance import build_provenance
            build_provenance(args.repo_root, args.artifact_manifest, args.out)
        elif args.scmd == 'repository-health':
            from .repository_health import build_repository_health
            build_repository_health(args.repo_root, args.out)
        elif args.scmd == 'build-report': sc_build_report(args.input, args.out)
        elif args.scmd == 'render': sc_render(args.input, args.out)
        elif args.scmd == 'validate': sc_validate(args.input)
    elif args.cmd == 'policy':
        if args.pcmd == 'validate-kernel':
            errs = validate_kernel(load_kernel(args.kernel))
            if errs:
                print('\n'.join(errs)); raise SystemExit(1)
            print('kernel valid')
        elif args.pcmd == 'evaluate':
            Path(args.out).write_text(json.dumps(evaluate_file(args.input, args.context_type), indent=2), encoding='utf-8')
        elif args.pcmd == 'evaluate-repo':
            out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
            files = sorted([x for x in Path(args.repo_root).rglob('*') if x.is_file() and x.suffix.lower() in {'.md', '.json', '.yml', '.yaml'}])
            for i, fp in enumerate(files):
                (out / f'decision_{i:04d}.json').write_text(json.dumps(evaluate_file(str(fp), 'auto'), indent=2), encoding='utf-8')
        elif args.pcmd == 'decision-log': write_decision_log(args.decisions, args.registry)
        elif args.pcmd in {'build-data', 'render'}: build_policy_data(args.registry, args.out)
        elif args.pcmd == 'export-opa': export_opa(args.kernel, args.out)


if __name__ == '__main__':
    main()
