import argparse
from pathlib import Path
from .core import run_gauntlet, replay_docket, audit_docket, build_safe_pr_materials, build_external_reviewer_kit


def main():
    p = argparse.ArgumentParser(prog='agialpha_phoenix_gauntlet')
    sub = p.add_subparsers(dest='cmd', required=True)

    r = sub.add_parser('run')
    r.add_argument('--repo-root', default='.')
    r.add_argument('--out', required=True)
    r.add_argument('--site-out', default=None)
    r.add_argument('--challenge-dir', default='phoenix_challenge_packs')
    r.add_argument('--run-id', default=None)
    r.add_argument('--commit', default=None)
    r.add_argument('--branch', default=None)
    r.add_argument('--actor', default=None)
    r.add_argument('--workflow', default=None)

    rp = sub.add_parser('replay')
    rp.add_argument('--docket', required=True)
    rp.add_argument('--out', required=True)

    a = sub.add_parser('audit')
    a.add_argument('--docket', required=True)
    a.add_argument('--out', required=True)
    a.add_argument('--strict', action='store_true')

    sp = sub.add_parser('safe-pr-materials')
    sp.add_argument('--docket', required=True)
    sp.add_argument('--out', required=True)

    er = sub.add_parser('external-review-kit')
    er.add_argument('--docket', required=True)
    er.add_argument('--out', required=True)

    args = p.parse_args()
    if args.cmd == 'run':
        run_gauntlet(Path(args.repo_root), Path(args.out), Path(args.site_out) if args.site_out else None, Path(args.challenge_dir), args)
    elif args.cmd == 'replay':
        replay_docket(Path(args.docket), Path(args.out))
    elif args.cmd == 'audit':
        audit_docket(Path(args.docket), Path(args.out), strict=args.strict)
    elif args.cmd == 'safe-pr-materials':
        build_safe_pr_materials(Path(args.docket), Path(args.out))
    elif args.cmd == 'external-review-kit':
        build_external_reviewer_kit(Path(args.docket), Path(args.out))

if __name__ == '__main__':
    main()
