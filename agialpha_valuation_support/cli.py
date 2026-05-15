from pathlib import Path
import argparse
from .core import build, validate, build_data
from .render import render_summary

def main():
 p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd', required=True)
 b=sp.add_parser('build'); b.add_argument('--repo-root',required=True); b.add_argument('--ascension-registry',required=True); b.add_argument('--comparables',required=True); b.add_argument('--market-context',default='config/valuation_support_market_context.example.json'); b.add_argument('--out',required=True)
 b.set_defaults(func=lambda a: build(Path(a.repo_root),Path(a.ascension_registry),Path(a.comparables),Path(a.market_context),Path(a.out)))
 v=sp.add_parser('validate'); v.add_argument('--run',required=True); v.set_defaults(func=lambda a: validate(Path(a.run)))
 d=sp.add_parser('build-data'); d.add_argument('--registry',required=True); d.add_argument('--out',required=True); d.set_defaults(func=lambda a: build_data(Path(a.registry),Path(a.out)))
 s=sp.add_parser('summarize'); s.add_argument('--run',required=True); s.add_argument('--out',required=True); s.set_defaults(func=lambda a: Path(a.out).write_text(render_summary(Path(a.run)), encoding='utf-8'))
 a=p.parse_args(); a.func(a)
