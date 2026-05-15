import argparse
from pathlib import Path
from .core import build, validate, build_data

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    b=sp.add_parser('build'); b.add_argument('--repo-root',required=True); b.add_argument('--ascension-registry',required=True); b.add_argument('--comparables',required=True); b.add_argument('--market-context',required=False, default=None); b.add_argument('--out',required=True)
    b.set_defaults(func=lambda a: build(Path(a.repo_root),Path(a.ascension_registry),Path(a.comparables),Path(a.market_context) if a.market_context else None,Path(a.out)))
    v=sp.add_parser('validate'); v.add_argument('--run',required=True); v.set_defaults(func=lambda a: validate(Path(a.run)))
    d=sp.add_parser('build-data'); d.add_argument('--registry',required=True); d.add_argument('--out',required=True); d.set_defaults(func=lambda a: build_data(Path(a.registry),Path(a.out)))
    s=sp.add_parser('summarize'); s.add_argument('--run',required=True); s.add_argument('--out',required=True); s.set_defaults(func=lambda a: Path(a.out).write_text('Valuation support summary\n',encoding='utf-8'))
    a=ap.parse_args(); a.func(a)
if __name__=='__main__':main()
