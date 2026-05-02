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

    aauto = sp.add_parser("autonomous")
    aauto.add_argument("--repo-root", default=".")
    aauto.add_argument("--cycles", type=int, default=3)
    aauto.add_argument("--candidate-niches", type=int, default=64)
    aauto.add_argument("--evaluate-niches", type=int, default=24)
    aauto.add_argument("--local-variants-per-niche", type=int, default=5)
    aauto.add_argument("--out", default="cyber-ga-sovereign-runs/autonomous")

    for cmd in ["safe-pr", "policy-pr", "delayed-outcome", "vnext"]:
        c = sp.add_parser(cmd)
        c.add_argument("--docket", default="cyber-ga-sovereign-runs/test/cyber-ga-sovereign-evidence-docket")

    r = sp.add_parser("replay"); r.add_argument("--docket", required=True)
    f = sp.add_parser("falsification-audit"); f.add_argument("--docket", required=True)
    a = p.parse_args()
    if a.cmd in {"lifecycle", "autonomous"}:
        wf_name = 'AGI ALPHA Cyber-GA Sovereign 001 / Autonomous' if a.cmd == 'autonomous' else 'AGI ALPHA Cyber-GA Sovereign 001 / Lifecycle'
        wf_file = '.github/workflows/cyber-ga-sovereign-001-autonomous.yml' if a.cmd == 'autonomous' else '.github/workflows/cyber-ga-sovereign-001-lifecycle.yml'
        run_lifecycle(Path(getattr(a, 'repo_root', '.')), getattr(a, 'cycles', 1), getattr(a, 'candidate_niches', 16), getattr(a, 'evaluate_niches', 6), getattr(a, 'local_variants_per_niche', 3), Path(getattr(a, 'out', 'cyber-ga-sovereign-runs/test')), wf_name, wf_file)
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
