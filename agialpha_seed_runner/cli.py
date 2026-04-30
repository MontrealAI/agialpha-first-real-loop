from __future__ import annotations

import argparse
from pathlib import Path
from . import core


def main() -> None:
    parser = argparse.ArgumentParser(prog="agialpha_seed_runner", description="AGI ALPHA Edge Seed Runner v0.2")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("run-seeds")
    p.add_argument("--base-docket", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--count", type=int, default=10)
    p.add_argument("--scoreboard", default="docs/seed-runner")

    p = sub.add_parser("independent-replay")
    p.add_argument("--docket-root", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--site", default="docs/independent-replay")

    p = sub.add_parser("falsification-audit")
    p.add_argument("--docket-root", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--site", default="docs/falsification-audit")

    p = sub.add_parser("landing")
    p.add_argument("--docs", default="docs")

    args = parser.parse_args()

    if args.cmd == "run-seeds":
        index = core.run_seed_runner(Path(args.base_docket), Path(args.out), args.count)
        core.build_seed_scoreboard(index, Path(args.scoreboard))
    elif args.cmd == "independent-replay":
        report = core.independent_replay(Path(args.docket_root), Path(args.out))
        # Copy built site to requested docs path
        src = Path(args.out) / "site"
        dst = Path(args.site)
        if dst.exists():
            import shutil; shutil.rmtree(dst)
        import shutil; shutil.copytree(src, dst)
    elif args.cmd == "falsification-audit":
        summary = core.aggregate_falsification(Path(args.docket_root), Path(args.out))
        src = Path(args.out) / "site"
        dst = Path(args.site)
        if dst.exists():
            import shutil; shutil.rmtree(dst)
        import shutil; shutil.copytree(src, dst)
    elif args.cmd == "landing":
        core.build_landing_page(Path(args.docs))


if __name__ == "__main__":
    main()
