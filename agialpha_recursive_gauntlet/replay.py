from .context import *


def generate_replay(run: Path, out: Path):
    required = [
        run / "03_candidate_lock/candidate_lock.json",
        run / "04_heldout_tasks/heldout_tasks.json",
        run / "05_evaluations/candidate_vs_incumbent.json",
    ]
    missing = [str(p) for p in required if not p.exists()]
    replay_pass = len(missing) == 0
    report = {
        "replay_pass": replay_pass,
        "claim_boundary": CLAIM_BOUNDARY,
        "checked": [str(p) for p in required],
        "missing": missing,
    }
    write_json(out, report)
    return report
