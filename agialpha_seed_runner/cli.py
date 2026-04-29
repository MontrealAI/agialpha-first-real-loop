
from __future__ import annotations

import argparse
from pathlib import Path

from .core import (
    CLAIM_BOUNDARY,
    build_seed_scoreboard,
    independent_replay,
    run_seed_runner,
)

def cmd_run_seeds(args: argparse.Namespace) -> int:
    index = run_seed_runner(Path(args.base_docket), Path(args.out), int(args.count))
    if args.scoreboard:
        build_seed_scoreboard(index, Path(args.scoreboard))
    print(f"seed-runner completed {index['count']} seed dockets at {args.out}")
    return 0

def cmd_independent_replay(args: argparse.Namespace) -> int:
    report = independent_replay(Path(args.docket_root), Path(args.out))
    print(f"independent replay checked {report['total_dockets']} dockets: {report['passed']} pass, {report['failed']} fail")
    return 0 if report["failed"] == 0 else 1

def cmd_claim_boundary(args: argparse.Namespace) -> int:
    print(CLAIM_BOUNDARY)
    return 0

def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="python -m agialpha_seed_runner")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("run-seeds")
    s.add_argument("--base-docket", default="evidence-docket")
    s.add_argument("--out", required=True)
    s.add_argument("--count", type=int, default=10)
    s.add_argument("--scoreboard")
    s.set_defaults(func=cmd_run_seeds)

    s = sub.add_parser("independent-replay")
    s.add_argument("--docket-root", required=True)
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_independent_replay)

    s = sub.add_parser("claim-boundary")
    s.set_defaults(func=cmd_claim_boundary)

    args = p.parse_args(argv)
    raise SystemExit(args.func(args))

if __name__ == "__main__":
    main()
