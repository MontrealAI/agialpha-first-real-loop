import argparse
from pathlib import Path
from . import core

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest="cmd", required=True)
    b=sp.add_parser("build"); b.add_argument("--repo-root", required=True); b.add_argument("--ascension-registry", required=True); b.add_argument("--comparables", required=True); b.add_argument("--out", required=True)
    b.set_defaults(func=lambda a: core.build(Path(a.repo_root), Path(a.ascension_registry), Path(a.comparables), Path(a.out)))
    bd=sp.add_parser("build-data"); bd.add_argument("--registry", required=True); bd.add_argument("--out", required=True); bd.set_defaults(func=lambda a: core.build_data(Path(a.registry), Path(a.out)))
    v=sp.add_parser("validate"); v.add_argument("--run", required=True); v.set_defaults(func=lambda a: core.validate(Path(a.run)))
    a=ap.parse_args(); a.func(a)
if __name__=="__main__": main()
