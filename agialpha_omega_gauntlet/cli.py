
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from .core import run_experiment, replay_docket, falsification_audit, scaling_proxy, write_json, CLAIM_BOUNDARY

def main(argv=None):
    p = argparse.ArgumentParser(prog="agialpha_omega_gauntlet")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--out", required=True)
    r.add_argument("--challenge-dir", default="omega_challenge_packs")
    r.add_argument("--no-clean", action="store_true")
    rp = sub.add_parser("replay")
    rp.add_argument("docket")
    rp.add_argument("--out")
    au = sub.add_parser("audit")
    au.add_argument("docket")
    au.add_argument("--out")
    sc = sub.add_parser("scaling")
    sc.add_argument("--out", required=True)
    safe = sub.add_parser("safe-pr-materials")
    safe.add_argument("docket")
    safe.add_argument("--out", required=True)
    args = p.parse_args(argv)
    if args.cmd == "run":
        summary = run_experiment(Path(args.out), Path(args.challenge_dir), clean=not args.no_clean)
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif args.cmd == "replay":
        res = replay_docket(Path(args.docket))
        if args.out: write_json(Path(args.out), res)
        print(json.dumps(res, indent=2, sort_keys=True))
        raise SystemExit(0 if res["status"] == "pass" else 1)
    elif args.cmd == "audit":
        res = falsification_audit(Path(args.docket))
        if args.out: write_json(Path(args.out), res)
        print(json.dumps(res, indent=2, sort_keys=True))
        raise SystemExit(0 if res["status"] == "pass" else 1)
    elif args.cmd == "scaling":
        res = scaling_proxy(Path(args.out))
        print(json.dumps(res, indent=2, sort_keys=True))
    elif args.cmd == "safe-pr-materials":
        src = Path(args.docket) / "16_safe_pr_materials"
        dst = Path(args.out)
        dst.mkdir(parents=True, exist_ok=True)
        if src.exists():
            for item in src.iterdir():
                if item.is_file():
                    shutil.copy2(item, dst / item.name)
        else:
            (dst / "README_SAFE_PR.md").write_text("# Safe PR materials\n\nNo existing material found.\n\nClaim boundary: " + CLAIM_BOUNDARY + "\n", encoding="utf-8")
        print(json.dumps({"status": "done", "out": str(dst)}, indent=2))

if __name__ == "__main__":
    main()
