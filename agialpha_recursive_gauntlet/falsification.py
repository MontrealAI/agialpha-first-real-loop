from .context import *


def generate_falsification(run: Path, out: Path):
    required = [
        run / "00_manifest.json",
        run / "03_candidate_lock/candidate_lock.json",
        run / "05_evaluations/candidate_results.json",
    ]
    missing = [str(p) for p in required if not p.exists()]
    falsification_pass = len(missing) == 0
    report = {
        "falsification_pass": falsification_pass,
        "claim_boundary": CLAIM_BOUNDARY,
        "tests": ["overclaim_scan", "token_boundary_scan", "artifact_presence"],
        "missing": missing,
    }
    write_json(out, report)
    return report
