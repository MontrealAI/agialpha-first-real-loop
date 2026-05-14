import argparse
from pathlib import Path
from . import core

def main() -> None:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)

    rc = sp.add_parser("run-cycle")
    rc.add_argument("--repo-root", required=True)
    rc.add_argument("--out", required=True)
    rc.add_argument("--registry", default="ascension_os_registry")
    rc.set_defaults(func=lambda a: core.run_cycle(Path(a.repo_root), Path(a.out), Path(a.registry)))

    oe = sp.add_parser("run-open-rsi-eval")
    oe.add_argument("--repo-root", required=True); oe.add_argument("--out", required=True); oe.add_argument("--task-count", type=int, default=16)
    oe.set_defaults(func=lambda a: core.run_open_rsi_eval(Path(a.out), a.task_count))

    gt = sp.add_parser("run-gauntlet")
    gt.add_argument("--repo-root", required=True); gt.add_argument("--out", required=True); gt.add_argument("--task-count", type=int, default=12)
    gt.set_defaults(func=lambda a: core.run_gauntlet(Path(a.out), a.task_count))

    vea = sp.add_parser("verified-enterprise-alpha"); vea.add_argument("--run", required=True)
    vea.set_defaults(func=lambda a: core.verified_enterprise_alpha(Path(a.run)))

    vtc = sp.add_parser("value-to-capacity"); vtc.add_argument("--run", required=True)
    vtc.set_defaults(func=lambda a: core.value_to_capacity(Path(a.run)))

    vs = sp.add_parser("valuation-support")
    vs.add_argument("--repo-root", required=True); vs.add_argument("--run", required=True); vs.add_argument("--out", required=True)
    vs.set_defaults(func=lambda a: core.valuation_support(Path(a.repo_root), Path(a.run), Path(a.out)))

    rp = sp.add_parser("replay"); rp.add_argument("--run", required=True); rp.set_defaults(func=lambda a: core.replay(Path(a.run)))
    fa = sp.add_parser("falsification-audit"); fa.add_argument("--run", required=True); fa.set_defaults(func=lambda a: core.falsification(Path(a.run)))
    vd = sp.add_parser("validate"); vd.add_argument("--run", required=True); vd.set_defaults(func=lambda a: core.validate(Path(a.run)))

    bd = sp.add_parser("build-data"); bd.add_argument("--registry", required=True); bd.add_argument("--out", required=True)
    bd.set_defaults(func=lambda a: core.build_data(Path(a.registry), Path(a.out)))

    args = ap.parse_args(); args.func(args)

if __name__ == "__main__":
    main()
