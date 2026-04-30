from __future__ import annotations

import argparse
from pathlib import Path

from .core import run_experiment, external_replay, scaling_run, audit_run, adapters_run


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="agialpha_helios2")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("run", help="Run HELIOS-002 autonomous experiment")
    p.add_argument("--out", required=True)
    p.add_argument("--source", default="evidence-docket")
    p.add_argument("--docs", default="")

    p = sub.add_parser("external-replay", help="Run HELIOS-002 external-review replay scaffold")
    p.add_argument("--out", required=True)
    p.add_argument("--source", default="")
    p.add_argument("--docs", default="")

    p = sub.add_parser("scaling", help="Generate HELIOS-002 L6 CI scaling proxy")
    p.add_argument("--out", required=True)
    p.add_argument("--docs", default="")

    p = sub.add_parser("audit", help="Run HELIOS-002 falsification audit")
    p.add_argument("--out", required=True)
    p.add_argument("--source", default="")
    p.add_argument("--docs", default="")

    p = sub.add_parser("adapters", help="Generate HELIOS-002 external benchmark adapters")
    p.add_argument("--out", required=True)
    p.add_argument("--docs", default="")

    args = parser.parse_args(argv)
    docs = Path(args.docs) if getattr(args, "docs", "") else None
    if args.cmd == "run":
        source = Path(args.source) if args.source else None
        summary = run_experiment(Path(args.out), source=source, docs=docs)
        print(f"HELIOS-002 complete: {summary['L_status']}")
    elif args.cmd == "external-replay":
        source = Path(args.source) if args.source else None
        report = external_replay(Path(args.out), source=source, docs=docs)
        print(f"HELIOS-002 external replay: {report['L4_status']}")
    elif args.cmd == "scaling":
        report = scaling_run(Path(args.out), docs=docs)
        print(f"HELIOS-002 scaling: {report['claim_level']}")
    elif args.cmd == "audit":
        source = Path(args.source) if args.source else None
        report = audit_run(Path(args.out), source=source, docs=docs)
        print(f"HELIOS-002 audit: {report['audit_status']}")
    elif args.cmd == "adapters":
        report = adapters_run(Path(args.out), docs=docs)
        print(f"HELIOS-002 adapters: {len(report['adapters'])} templates generated")
    return 0
