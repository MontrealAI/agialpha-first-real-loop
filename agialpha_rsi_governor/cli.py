import argparse
import json
import time
import sys
from pathlib import Path

from .candidates import generate_candidates
from .dossier import promotion_md
from .evaluator import eval_kernel
from .kernel import kernel_hash, load_kernel
from .promotion import promotion_gate
from .render import scoreboard_html
from .replay import replay_docket
from .falsification import falsification_report
from .canary import default_canary_report


POLICY_FORBIDDEN_AUTONOMOUS_ACTIONS = {
    "merge_pr",
    "enable_automerge",
    "persist_kernel_without_pr",
    "delete_rejected_candidates",
    "hide_failed_evaluations",
    "relax_claim_boundaries",
    "mark_missing_metrics_as_zero",
    "execute_downloaded_artifact_code",
    "deploy_pages_directly_from_rsi_workflow",
}


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
    result = replay_docket(d)
    print(json.dumps(result))
    if not result["replay_pass"]:
        raise SystemExit(1)


def falsification_audit(docket: str):
    d = Path(docket)
    result = falsification_report(d)
    print(json.dumps(result))
    if not result["falsification_pass"]:
        raise SystemExit(1)


def lifecycle(repo_root: str, out: str):
    run(repo_root, out)

def vnext_canary(repo_root: str, out: str):
    p=Path(out); p.mkdir(parents=True, exist_ok=True)
    report=default_canary_report()
    (p/"vnext_canary_report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report))


def validate_autonomy_contract(contract: str):
    payload = json.loads(Path(contract).read_text())

    def _require_action_list(field: str) -> list[str]:
        value = payload.get(field)
        if not isinstance(value, list):
            raise SystemExit(f"invalid {field}: expected JSON array of action strings")
        if not all(isinstance(x, str) for x in value):
            raise SystemExit(f"invalid {field}: all actions must be strings")
        return value

    required = {
        "schema_version": "agialpha.rsi_governor_autonomy_contract.v1",
        "experiment_slug": "rsi-governor-001",
    }
    for key, val in required.items():
        if payload.get(key) != val:
            raise SystemExit(f"invalid {key}: expected {val}")

    required_pre = {
        "run_replay",
        "run_falsification_audit",
        "open_safe_pr_if_candidate_passes",
        "notify_evidence_hub_publisher",
    }
    required_post = {
        "run_delayed_outcome_sentinel",
        "run_vnext_canary",
        "notify_evidence_hub_publisher",
    }
    pre = set(_require_action_list("autonomous_pre_promotion_actions"))
    post = set(_require_action_list("autonomous_post_merge_actions"))
    contract_forbidden_auto = set(_require_action_list("forbidden_autonomous_actions"))
    missing_forbidden_policy_actions = sorted(POLICY_FORBIDDEN_AUTONOMOUS_ACTIONS - contract_forbidden_auto)
    if missing_forbidden_policy_actions:
        raise SystemExit(
            "contract missing required forbidden_autonomous_actions policy entries: "
            + ", ".join(missing_forbidden_policy_actions)
        )

    forbidden_overlap = sorted((pre | post) & POLICY_FORBIDDEN_AUTONOMOUS_ACTIONS)
    if forbidden_overlap:
        raise SystemExit(
            "forbidden autonomous actions present in autonomous action lists: "
            + ", ".join(forbidden_overlap)
        )

    missing_pre = sorted(required_pre - pre)
    missing_post = sorted(required_post - post)
    if missing_pre or missing_post:
        raise SystemExit(
            "contract requires manual chaining for: "
            + ", ".join(missing_pre + missing_post)
        )

    op = set(_require_action_list("operator_required_actions"))
    forbidden_manual = {
        "run_replay",
        "run_falsification_audit",
        "open_safe_pr_if_candidate_passes",
        "run_delayed_outcome_sentinel",
        "run_vnext_canary",
        "notify_evidence_hub_publisher",
    }
    overlap = sorted(op & forbidden_manual)
    if overlap:
        raise SystemExit(f"forbidden manual actions present: {', '.join(overlap)}")

    print(json.dumps({"status": "ok", "contract": contract}))


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
    c = sp.add_parser("validate-autonomy-contract")
    c.add_argument("--contract", required=True)
    a = p.parse_args()
    {
        "run": lambda: run(a.repo_root, a.out),
        "replay": lambda: replay(a.docket),
        "falsification-audit": lambda: falsification_audit(a.docket),
        "lifecycle": lambda: lifecycle(a.repo_root, a.out),
        "vnext-canary": lambda: vnext_canary(a.repo_root, a.out),
        "validate-autonomy-contract": lambda: validate_autonomy_contract(a.contract),
    }[a.cmd]()


if __name__ == "__main__":
    main()
