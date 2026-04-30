from __future__ import annotations
import argparse
from .core import run_experiment, replay, falsification_audit, build_scoreboard, scaling, adapters, delayed


def main() -> None:
    p = argparse.ArgumentParser(prog="agialpha_helios3")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--out", required=True)
    rp = sub.add_parser("replay")
    rp.add_argument("--root", required=True)
    rp.add_argument("--out", default=None)
    fa = sub.add_parser("falsification")
    fa.add_argument("--root", required=True)
    sc = sub.add_parser("scoreboard")
    sc.add_argument("--root", required=True)
    sc.add_argument("--docs", required=True)
    sg = sub.add_parser("scaling")
    sg.add_argument("--out", required=True)
    ad = sub.add_parser("adapters")
    ad.add_argument("--out", required=True)
    de = sub.add_parser("delayed")
    de.add_argument("--root", required=True)
    de.add_argument("--out", default=None)
    args = p.parse_args()
    if args.cmd == "run":
        print(run_experiment(args.out))
    elif args.cmd == "replay":
        print(replay(args.root, args.out))
    elif args.cmd == "falsification":
        print(falsification_audit(args.root))
    elif args.cmd == "scoreboard":
        print(build_scoreboard(args.root, args.docs))
    elif args.cmd == "scaling":
        print(scaling(args.out))
    elif args.cmd == "adapters":
        print(adapters(args.out))
    elif args.cmd == "delayed":
        print(delayed(args.root, args.out))
