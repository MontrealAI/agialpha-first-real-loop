from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .core import (
    BASE_REQUIRED,
    CLAIM_BOUNDARY,
    build_scoreboard,
    complete_docket,
    ensure_base_docket,
    lint_docket,
    make_replay_report,
    next_seed_payload,
    seed_matrix,
    scaling_curve,
    write_json,
)


def run_shell(command: str, env: dict[str, str] | None = None) -> int:
    print(f"[evidence-factory] $ {command}", flush=True)
    return subprocess.call(command, shell=True, env=env)


def cmd_lint(args: argparse.Namespace) -> int:
    result = lint_docket(Path(args.docket), strict=args.strict)
    if args.out:
        write_json(Path(args.out), result)
    print(result)
    return 0 if result["status"] == "pass" else 1


def cmd_seed_docket(args: argparse.Namespace) -> int:
    out = Path(args.out)
    if out.exists() and not args.force:
        print(f"Refusing to overwrite existing {out}; pass --force", file=sys.stderr)
        return 2
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    ensure_base_docket(out)
    print(f"Seed docket written to {out}")
    return 0


def cmd_run_or_seed(args: argparse.Namespace) -> int:
    out = Path(args.out)
    env = dict(os.environ)
    env["DOCKET_DIR"] = str(out)
    if out.exists() and args.clean:
        shutil.rmtree(out)
    if args.command:
        rc = run_shell(args.command, env=env)
        if rc == 0 and all((out / name).exists() for name in BASE_REQUIRED):
            print(f"Loop command produced a base Evidence Docket at {out}")
            return 0
        print(f"Loop command did not produce a complete base docket; rc={rc}. Falling back to seed docket.")
    ensure_base_docket(out)
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    actual = Path(args.actual_replay) if args.actual_replay else None
    complete_docket(Path(args.docket), Path(args.out) if args.out else None, actual)
    print("completed")
    return 0


def cmd_replay_report(args: argparse.Namespace) -> int:
    report = make_replay_report(Path(args.expected), Path(args.actual) if args.actual else None)
    write_json(Path(args.out), report)
    print(report)
    return 0 if report.get("status") in {"pass", "pending"} else 1


def cmd_seed_matrix(args: argparse.Namespace) -> int:
    result = seed_matrix(Path(args.docket), Path(args.out), args.count)
    print(result)
    return 0


def cmd_scaling(args: argparse.Namespace) -> int:
    result = scaling_curve(Path(args.out))
    print(f"wrote {len(result['rows'])} proxy rows")
    return 0


def cmd_scoreboard(args: argparse.Namespace) -> int:
    dockets = [Path(x) for x in args.dockets]
    if args.scan:
        for root in args.scan:
            rp = Path(root)
            if rp.exists():
                dockets.extend([p.parent for p in rp.rglob("00_manifest.json") if p.is_file()])
    index = build_scoreboard(dockets, Path(args.out))
    print(f"scoreboard runs={len(index['runs'])}")
    return 0


def cmd_next_seed(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    payload = next_seed_payload(Path(args.docket))
    target = out / f"next_seed_{os.environ.get('GITHUB_RUN_ID','local')}.json"
    write_json(target, payload)
    print(f"next seed proposal: {target}")
    return 0


def cmd_print_boundary(args: argparse.Namespace) -> int:
    print(CLAIM_BOUNDARY)
    return 0


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="python -m agialpha_evidence_factory")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("lint")
    s.add_argument("docket")
    s.add_argument("--strict", action="store_true")
    s.add_argument("--out")
    s.set_defaults(func=cmd_lint)

    s = sub.add_parser("seed-docket")
    s.add_argument("--out", required=True)
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_seed_docket)

    s = sub.add_parser("run-or-seed")
    s.add_argument("--out", required=True)
    s.add_argument("--command", default="")
    s.add_argument("--clean", action="store_true")
    s.set_defaults(func=cmd_run_or_seed)

    s = sub.add_parser("complete")
    s.add_argument("docket")
    s.add_argument("--out")
    s.add_argument("--actual-replay")
    s.set_defaults(func=cmd_complete)

    s = sub.add_parser("replay-report")
    s.add_argument("--expected", required=True)
    s.add_argument("--actual")
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_replay_report)

    s = sub.add_parser("seed-matrix")
    s.add_argument("docket")
    s.add_argument("--out", required=True)
    s.add_argument("--count", type=int, default=10)
    s.set_defaults(func=cmd_seed_matrix)

    s = sub.add_parser("scaling-curve")
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_scaling)

    s = sub.add_parser("scoreboard")
    s.add_argument("dockets", nargs="*")
    s.add_argument("--scan", nargs="*", default=[])
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_scoreboard)

    s = sub.add_parser("next-seed")
    s.add_argument("docket")
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_next_seed)

    s = sub.add_parser("claim-boundary")
    s.set_defaults(func=cmd_print_boundary)

    args = p.parse_args(argv)
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
