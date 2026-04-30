from __future__ import annotations

import argparse
from pathlib import Path
from . import core


def main() -> None:
    parser = argparse.ArgumentParser(prog="agialpha_helios", description="AGI ALPHA HELIOS-001 autonomous Evidence Docket experiment")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run HELIOS-001 and produce Evidence Dockets")
    p_run.add_argument("--out", default="runs/helios/latest")
    p_run.add_argument("--publish-dir", default="")

    p_replay = sub.add_parser("replay", help="Replay/check HELIOS-001 artifact")
    p_replay.add_argument("--source", default="runs/helios/latest")
    p_replay.add_argument("--out", default="")

    p_audit = sub.add_parser("audit", help="Run falsification audit")
    p_audit.add_argument("--source", default="runs/helios/latest")
    p_audit.add_argument("--out", default="")

    p_vnext = sub.add_parser("vnext", help="Run vNext transfer report")
    p_vnext.add_argument("--source", default="runs/helios/latest")
    p_vnext.add_argument("--out", default="runs/helios-vnext/latest")

    args = parser.parse_args()
    if args.cmd == "run":
        summary = core.run(Path(args.out), Path(args.publish_dir) if args.publish_dir else None)
        print(core.canonical_json(summary))
    elif args.cmd == "replay":
        report = core.replay(Path(args.source), Path(args.out) if args.out else None)
        print(core.canonical_json(report))
    elif args.cmd == "audit":
        report = core.falsification_audit(Path(args.source))
        if args.out:
            Path(args.out).mkdir(parents=True, exist_ok=True)
            core.write_json(Path(args.out) / "helios_falsification_audit_report.json", report)
        print(core.canonical_json(report))
    elif args.cmd == "vnext":
        report = core.vnext_transfer(Path(args.source), Path(args.out))
        print(core.canonical_json(report))

if __name__ == "__main__":
    main()
