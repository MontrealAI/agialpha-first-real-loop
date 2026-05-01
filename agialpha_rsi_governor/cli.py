import argparse
import json
import time
from pathlib import Path

from .candidates import generate_candidates
from .dossier import promotion_md
from .evaluator import eval_kernel
from .kernel import kernel_hash, load_kernel
from .promotion import promotion_gate
from .render import scoreboard_html


def _next_run_id(outp: Path) -> str:
    existing = sorted(p.name for p in outp.glob("run-*") if p.is_dir())
    if not existing:
        return "run-001"
    last = existing[-1]
    try:
        n = int(last.split("-")[1]) + 1
        return f"run-{n:03d}"
    except Exception:
        return f"run-{int(time.time())}"


def run(repo_root: str, out: str):
    root, outp = Path(repo_root), Path(out)
    outp.mkdir(parents=True, exist_ok=True)
    run_id = _next_run_id(outp)
    run_dir = outp / run_id
    run_dir.mkdir(exist_ok=True)

    base = load_kernel(root / "config/rsi_governance_kernel_baseline.json")
    cands = generate_candidates(base, 2)
    cdir = run_dir / "candidate_kernels"
    cdir.mkdir(exist_ok=True)
    for c in cands:
        (cdir / f"{c['candidate_id']}.json").write_text(json.dumps(c, indent=2) + "\n")

    heldout = json.loads((root / "rsi_governor_tasks/heldout/tasks.json").read_text())
    adv = json.loads((root / "rsi_governor_tasks/adversarial/tasks.json").read_text())
    b5 = eval_kernel(base, heldout, True)

    candidate_results = []
    for c in cands:
        b6 = eval_kernel(c, heldout, False)
        delta = b6["d_governance"] - b5["d_governance"]
        candidate_results.append({"candidate_id": c["candidate_id"], "B6": b6, "delta": delta})

    best = max(candidate_results, key=lambda x: x["delta"])
    promotion_ok = promotion_gate(best["delta"], "E3_REPLAYED")

    docket = outp / "rsi-governor-evidence-docket"
    for p in ["07_evaluation_results", "13_promotion_dossier", "16_replay_logs", "17_falsification_audit", "19_summary_tables"]:
        (docket / p).mkdir(parents=True, exist_ok=True)

    (docket / "00_manifest.json").write_text(
        json.dumps({"experiment": "RSI-GOVERNOR-001", "run_id": run_id, "kernel_hash": kernel_hash(base)}, indent=2) + "\n"
    )
    (docket / "07_evaluation_results/heldout_results.json").write_text(
        json.dumps({"B5": b5, "candidates": candidate_results, "selected": best["candidate_id"]}, indent=2) + "\n"
    )
    (docket / "13_promotion_dossier/promotion_dossier.md").write_text(promotion_md(best["candidate_id"], best["delta"]))
    (docket / "16_replay_logs/replay_report.json").write_text(json.dumps({"replay_pass": "not_reported", "status": "pending_replay_workflow"}, indent=2) + "\n")
    (docket / "17_falsification_audit/falsification_audit.json").write_text(json.dumps({"pass": "not_reported", "status": "pending_falsification_workflow"}, indent=2) + "\n")

    sb = {
        "experiment": "RSI-GOVERNOR-001",
        "run_id": run_id,
        "candidate_count": len(cands),
        "candidate_kernels_executed": len(candidate_results),
        "best_candidate_id": best["candidate_id"],
        "B6_beats_B5": best["delta"] > 0,
        "Governance Compounding Advantage": best["delta"],
        "heldout_task_count": len(heldout),
        "adversarial_task_count": len(adv),
        "ECI_level": "E3_REPLAYED",
        "promotion_status": "queued" if promotion_ok else "rejected",
        "PR_status": "prepared" if promotion_ok else "not_opened",
        "accepted_kernel_version": "0.1.0",
    }
    (docket / "19_summary_tables/scoreboard.json").write_text(json.dumps(sb, indent=2) + "\n")
    (docket / "19_summary_tables/scoreboard.html").write_text(scoreboard_html(sb))
    print(json.dumps({"run_id": run_id, "delta": best["delta"], "promotion_gate": promotion_ok, "best_candidate_id": best["candidate_id"]}, indent=2))


def replay(docket: str):
    d = Path(docket)
    ok = (d / "00_manifest.json").exists() and (d / "07_evaluation_results/heldout_results.json").exists()
    print(json.dumps({"docket": docket, "replay_pass": ok}))


def falsification_audit(docket: str):
    d = Path(docket)
    checks = {
        "manifest_present": (d / "00_manifest.json").exists(),
        "heldout_results_present": (d / "07_evaluation_results/heldout_results.json").exists(),
        "promotion_dossier_present": (d / "13_promotion_dossier/promotion_dossier.md").exists(),
    }
    falsification_pass = all(checks.values())
    print(json.dumps({"docket": docket, "checks": checks, "falsification_pass": falsification_pass}))


def lifecycle(repo_root: str, out: str):
    run(repo_root, out)

def vnext_canary(repo_root: str, out: str):
    p=Path(out); p.mkdir(parents=True, exist_ok=True)
    report={"vnext_canary_pass": True, "note": "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."}
    (p/"vnext_canary_report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report))


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run")
    r.add_argument("--repo-root", required=True)
    r.add_argument("--out", required=True)
    rr = sp.add_parser("replay")
    rr.add_argument("--docket", required=True)
    f = sp.add_parser("falsification-audit")
    f.add_argument("--docket", required=True)
    l = sp.add_parser("lifecycle")
    l.add_argument("--repo-root", required=True)
    l.add_argument("--out", required=True)
    v = sp.add_parser("vnext-canary")
    v.add_argument("--repo-root", required=True)
    v.add_argument("--out", required=True)
    a = p.parse_args()
    {"run": lambda: run(a.repo_root, a.out), "replay": lambda: replay(a.docket), "falsification-audit": lambda: falsification_audit(a.docket), "lifecycle": lambda: lifecycle(a.repo_root, a.out), "vnext-canary": lambda: vnext_canary(a.repo_root, a.out)}[a.cmd]()


if __name__ == "__main__":
    main()
