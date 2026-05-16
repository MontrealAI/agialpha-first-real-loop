import argparse
from pathlib import Path
from .core import build, validate, build_data, replay, falsification_audit, emit_manifest
from .render import render_summary


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)

    b = sp.add_parser("build")
    b.add_argument("--repo-root", required=True)
    b.add_argument("--use-cases")
    b.add_argument("--out", required=True)
    b.add_argument("--registry", default="enterprise_pilot_registry")
    b.add_argument("--workflow-family")
    b.add_argument("--customer-mode")
    b.set_defaults(func=lambda a: build(Path(a.repo_root), Path(a.out), Path(a.use_cases or "config/enterprise_pilot_use_cases.example.json"), Path(a.registry)))

    v = sp.add_parser("validate"); v.add_argument("--run", required=True); v.set_defaults(func=lambda a: validate(Path(a.run)))
    r = sp.add_parser("replay"); r.add_argument("--run", required=True); r.set_defaults(func=lambda a: replay(Path(a.run)))
    f = sp.add_parser("falsification-audit"); f.add_argument("--run", required=True); f.set_defaults(func=lambda a: falsification_audit(Path(a.run)))
    d = sp.add_parser("build-data"); d.add_argument("--registry", required=True); d.add_argument("--out", required=True); d.set_defaults(func=lambda a: build_data(Path(a.registry), Path(a.out)))
    e = sp.add_parser("emit-manifest"); e.add_argument("--run", required=True); e.add_argument("--out", required=True); e.set_defaults(func=lambda a: emit_manifest(Path(a.run), Path(a.out)))
    s = sp.add_parser("summarize"); s.add_argument("--run", required=True); s.add_argument("--out", required=True); s.set_defaults(func=lambda a: Path(a.out).write_text(render_summary(Path(a.run)), encoding="utf-8"))
    a = p.parse_args(); a.func(a)
