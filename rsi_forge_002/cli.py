from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from .core import run_experiment, replay, load_kernel, load_state, write_json, default_kernel, default_state

def main(argv=None):
    p = argparse.ArgumentParser(prog="rsi_forge_002")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--out", required=True)
    r.add_argument("--repo-root", default=".")
    r.add_argument("--cycles", type=int, default=5)
    r.add_argument("--candidates", type=int, default=18)
    r.add_argument("--seed", type=int, default=37)
    r.add_argument("--no-patch", action="store_true")
    rep = sub.add_parser("replay")
    rep.add_argument("--docket", required=True)
    init = sub.add_parser("init")
    init.add_argument("--repo-root", default=".")
    args = p.parse_args(argv)
    if args.cmd == "run":
        res = run_experiment(Path(args.out), Path(args.repo_root), args.cycles, args.candidates, args.seed, not args.no_patch)
        print(json.dumps(res["summary"], indent=2, sort_keys=True))
    elif args.cmd == "replay":
        print(json.dumps(replay(Path(args.docket)), indent=2, sort_keys=True))
    elif args.cmd == "init":
        root = Path(args.repo_root)
        write_json(root/"data/rsi_forge_002/current_kernel.json", default_kernel())
        write_json(root/"data/rsi_forge_002/latest_state.json", default_state(default_kernel()))
        print("initialized data/rsi_forge_002")
if __name__ == "__main__":
    main()
