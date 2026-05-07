from __future__ import annotations
import argparse
from pathlib import Path
from .discover import discover
from .registry import build_indexes
from .validate import validate_registry
from .render import build_data, render_html
from .token_boundary import check_token_boundary


def main() -> int:
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd', required=True)
    for name in ('discover','validate-registry','check-work-vaults'):
        s=sp.add_parser(name); s.add_argument('--registry', required=True)
        if name=='discover': s.add_argument('--repo-root', required=True)
    bd=sp.add_parser('build-data'); bd.add_argument('--registry', required=True); bd.add_argument('--out', required=True)
    rd=sp.add_parser('render'); rd.add_argument('--registry', required=True); rd.add_argument('--out', required=True)
    tk=sp.add_parser('check-token-boundary'); tk.add_argument('--repo-root', required=True)
    a=p.parse_args()
    if a.cmd=='discover':
        discover(Path(a.repo_root), Path(a.registry)); build_indexes(Path(a.registry)); return 0
    if a.cmd in ('validate-registry','check-work-vaults'):
        return 0 if validate_registry(Path(a.registry)) else 1
    if a.cmd=='build-data':
        build_data(Path(a.registry), Path(a.out)); return 0
    if a.cmd=='render':
        render_html(Path(a.registry), Path(a.out)); return 0
    if a.cmd=='check-token-boundary':
        return 0 if check_token_boundary(Path(a.repo_root)) else 1
    return 1
