import argparse
from pathlib import Path

from .artifact_manifest import build_manifest
from .discover import discover
from .provenance import build_provenance
from .registry import build_indexes
from .render import build_data, render_html
from .repository_health import build_repository_health
from .supply_chain import build_report, collect, render as sc_render, validate
from .token_boundary import check_token_boundary
from .validate import validate_registry


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd', required=True)

    sc = sp.add_parser('supply-chain')
    ssp = sc.add_subparsers(dest='sub', required=True)
    c = ssp.add_parser('collect'); c.add_argument('--repo-root', required=True); c.add_argument('--out', required=True)
    h = ssp.add_parser('hash-artifacts'); h.add_argument('--repo-root', default='.'); h.add_argument('--input', required=True); h.add_argument('--out', required=True)
    pr = ssp.add_parser('provenance'); pr.add_argument('--repo-root', required=True); pr.add_argument('--artifact-manifest', required=True); pr.add_argument('--out', required=True)
    rh = ssp.add_parser('repository-health'); rh.add_argument('--repo-root', required=True); rh.add_argument('--out', required=True)
    br = ssp.add_parser('build-report'); br.add_argument('--input', required=True); br.add_argument('--out', required=True)
    r = ssp.add_parser('render'); r.add_argument('--input', required=True); r.add_argument('--out', required=True)
    v = ssp.add_parser('validate'); v.add_argument('--input', required=True)

    d = sp.add_parser('discover'); d.add_argument('--repo-root', required=True); d.add_argument('--registry', required=True)
    bd = sp.add_parser('build-data'); bd.add_argument('--registry', required=True); bd.add_argument('--out', required=True)
    rr = sp.add_parser('render'); rr.add_argument('--registry', required=True); rr.add_argument('--out', required=True)
    vr = sp.add_parser('validate-registry'); vr.add_argument('--registry', required=True)
    ctb = sp.add_parser('check-token-boundary'); ctb.add_argument('--repo-root', required=True)

    a = p.parse_args()

    if a.cmd == 'supply-chain':
        if a.sub == 'collect':
            collect(a.repo_root, a.out)
        elif a.sub == 'hash-artifacts':
            out_parent = str(Path(a.out).parent)
            manifest = build_manifest(a.repo_root, out_parent)
            Path(a.out).write_text(__import__('json').dumps(manifest, indent=2), encoding='utf-8')
        elif a.sub == 'provenance':
            build_provenance(a.repo_root, a.artifact_manifest, a.out)
        elif a.sub == 'repository-health':
            build_repository_health(a.repo_root, a.out)
        elif a.sub == 'build-report':
            build_report(a.input, a.out)
        elif a.sub == 'render':
            sc_render(a.input, a.out)
        elif a.sub == 'validate':
            validate(a.input)
        return

    if a.cmd == 'discover':
        discover(Path(a.repo_root), Path(a.registry))
        build_indexes(Path(a.registry))
        return
    if a.cmd == 'build-data':
        build_data(Path(a.registry), Path(a.out))
        return
    if a.cmd == 'render':
        render_html(Path(a.registry), Path(a.out))
        return
    if a.cmd == 'validate-registry':
        raise SystemExit(0 if validate_registry(Path(a.registry)) else 1)
    if a.cmd == 'check-token-boundary':
        raise SystemExit(0 if check_token_boundary(Path(a.repo_root)) else 1)
