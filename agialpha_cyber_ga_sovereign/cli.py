from __future__ import annotations
import argparse
from pathlib import Path
from .lifecycle import run_lifecycle
from .replay import run_replay
from .falsification import run_falsification
from .lifecycle import write_json, disclaimer


def main():
    p = argparse.ArgumentParser(prog="agialpha_cyber_ga_sovereign")
    sp = p.add_subparsers(dest="cmd", required=True)
    l = sp.add_parser("lifecycle")
    l.add_argument("--repo-root", default=".")
    l.add_argument("--cycles", type=int, default=3)
    l.add_argument("--candidate-niches", type=int, default=64)
    l.add_argument("--evaluate-niches", type=int, default=24)
    l.add_argument("--local-variants-per-niche", type=int, default=5)
    l.add_argument("--out", default="cyber-ga-sovereign-runs/test")

    a0 = sp.add_parser("autonomous")
    a0.add_argument("--repo-root", default=".")
    a0.add_argument("--cycles", type=int, default=3)
    a0.add_argument("--candidate-niches", type=int, default=64)
    a0.add_argument("--evaluate-niches", type=int, default=24)
    a0.add_argument("--local-variants-per-niche", type=int, default=5)
    a0.add_argument("--docket", default="cyber-ga-sovereign-runs/test/cyber-ga-sovereign-evidence-docket")

    for cmd in ["safe-pr", "policy-pr", "delayed-outcome", "vnext"]:
        c = sp.add_parser(cmd)
        c.add_argument("--docket", default="cyber-ga-sovereign-runs/test/cyber-ga-sovereign-evidence-docket")

    r = sp.add_parser("replay"); r.add_argument("--docket", required=True)
    f = sp.add_parser("falsification-audit"); f.add_argument("--docket", required=True)
    a = p.parse_args()
    if a.cmd == "lifecycle":
        run_lifecycle(Path(a.repo_root), a.cycles, a.candidate_niches, a.evaluate_niches, a.local_variants_per_niche, Path(a.out))
    elif a.cmd == "autonomous":
        out = Path(a.docket).parent
        run_lifecycle(Path(a.repo_root), a.cycles, a.candidate_niches, a.evaluate_niches, a.local_variants_per_niche, out)
    elif a.cmd == "replay":
        result = run_replay(Path(a.docket))
        if result.get("status") != "pass":
            raise SystemExit(1)
    elif a.cmd == "falsification-audit":
        result = run_falsification(Path(a.docket))
        if result.get("status") != "pass":
            raise SystemExit(1)
    else:
        d = Path(a.docket)
        write_json(d / f"{a.cmd.replace('-', '_')}.json", {"status": "pending_human_review", "claim_boundary": disclaimer(), "automerge": False})

if __name__ == "__main__":
    main()
