from __future__ import annotations

import argparse
import pathlib
from .core import run_frontier, replay_portfolio, falsification_audit, write_json


def main() -> None:
    parser = argparse.ArgumentParser(prog='agialpha_usefulness_frontier')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_run = sub.add_parser('run')
    p_run.add_argument('--repo', default='.')
    p_run.add_argument('--out', default='runs/frontier-usefulness/latest')
    p_run.add_argument('--apply-patches', action='store_true')

    p_replay = sub.add_parser('replay')
    p_replay.add_argument('--portfolio', default='runs/frontier-usefulness/latest')
    p_replay.add_argument('--out', default='runs/frontier-usefulness-replay/latest')

    p_audit = sub.add_parser('audit')
    p_audit.add_argument('--portfolio', default='runs/frontier-usefulness/latest')
    p_audit.add_argument('--out', default='runs/frontier-usefulness-audit/latest')

    args = parser.parse_args()
    if args.cmd == 'run':
        result = run_frontier(args.repo, args.out, apply_patches=args.apply_patches)
        print(result['summary'])
    elif args.cmd == 'replay':
        result = replay_portfolio(args.portfolio, args.out)
        print(result)
    elif args.cmd == 'audit':
        out = pathlib.Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        result = falsification_audit(out, pathlib.Path(args.portfolio))
        print(result)

if __name__ == '__main__':
    main()
