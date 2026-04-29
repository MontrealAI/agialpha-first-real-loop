from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Iterable

BASE_REQUIRED = [
    "00_manifest.json",
    "01_seed_001.json",
    "02_mark_review_card.json",
    "03_sovereign_001.json",
    "04_job_outputs.json",
    "05_sources_used.json",
    "06_accepted_interventions.json",
    "07_coldchain_energy_compiler_v0.json",
    "08_seed_002.json",
    "09_treatment_control_comparison.json",
    "10_decision_memo.md",
    "REPLAY_INSTRUCTIONS.md",
]

PUBLICATION_REQUIRED = [
    "11_cost_ledger.json",
    "12_safety_ledger.json",
    "13_baseline_results.json",
    "14_replay_report.json",
    "15_hash_manifest.json",
    "16_independent_review.md",
    "17_state_for_next_run.json",
    "18_source_snapshot.json",
    "19_claim_boundary.json",
    "claim_level.json",
]

CLAIM_LEVELS = [
    {"level": "L0", "name": "Architecture only", "description": "Formal system described."},
    {"level": "L1", "name": "Implementation scaffold", "description": "Code exists and can be inspected or run locally."},
    {"level": "L2", "name": "CI replay scaffold", "description": "GitHub Actions runs a deterministic loop and uploads an artifact."},
    {"level": "L3", "name": "Evidence Docket scaffold", "description": "Run produces manifest, job outputs, review card, compiler, comparison, decision memo, and replay instructions."},
    {"level": "L3.5", "name": "Internal clean-CI replay", "description": "A clean CI job replays the docket, but no independent reviewer has signed off yet."},
    {"level": "L4", "name": "Independently replayed Evidence Docket", "description": "An independent reviewer or clean external fork reproduces the docket."},
    {"level": "L5", "name": "Baseline-comparative evidence", "description": "Full baseline suite B0-B4 is run under equal constraints and the AGI ALPHA loop wins without worse safety."},
    {"level": "L6", "name": "Scaling evidence", "description": "More agents/nodes improve verified work per cost or task coverage without unacceptable overhead."},
    {"level": "L7", "name": "Real-task portfolio evidence", "description": "Runs across software, web/API, data/science, and protocol-native tasks."},
    {"level": "L8", "name": "External validation", "description": "External benchmark, delayed outcome, or independent validator confirms the result."},
]

CLAIM_BOUNDARY = (
    "This artifact does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, "
    "standard-setting control, guaranteed economic return, or civilization-scale capability. "
    "It records a bounded Evidence Docket. Stronger claims require independent replay, full baselines, "
    "cost/safety ledger review, delayed outcomes, and independent audit."
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def now_epoch() -> int:
    return int(time.time())


def git(cmd: list[str], cwd: Path | None = None) -> str:
    try:
        return subprocess.check_output(["git", *cmd], cwd=str(cwd) if cwd else None, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def source_snapshot(repo: Path | None = None) -> dict[str, Any]:
    repo = repo or Path.cwd()
    return {
        "schema": "agialpha.source_snapshot.v1",
        "generated_at_epoch": now_epoch(),
        "repository": os.environ.get("GITHUB_REPOSITORY", git(["remote", "get-url", "origin"], repo)),
        "commit": os.environ.get("GITHUB_SHA", git(["rev-parse", "HEAD"], repo)),
        "branch": os.environ.get("GITHUB_REF_NAME", git(["rev-parse", "--abbrev-ref", "HEAD"], repo)),
        "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "0"),
        "workflow": os.environ.get("GITHUB_WORKFLOW", "local"),
        "actor": os.environ.get("GITHUB_ACTOR", "local"),
        "dirty_status": git(["status", "--porcelain"], repo),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def validate_json_files(docket: Path) -> list[str]:
    errors: list[str] = []
    for p in sorted(docket.glob("*.json")):
        try:
            read_json(p)
        except Exception as exc:
            errors.append(f"invalid json: {p.name}: {exc}")
    return errors


def lint_docket(docket: Path, strict: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    for name in BASE_REQUIRED:
        if not (docket / name).exists():
            errors.append(f"missing base required file: {name}")
    if strict:
        for name in PUBLICATION_REQUIRED:
            if not (docket / name).exists():
                errors.append(f"missing publication required file: {name}")
    else:
        for name in PUBLICATION_REQUIRED:
            if not (docket / name).exists():
                warnings.append(f"missing publication file: {name}")
    errors.extend(validate_json_files(docket))
    if (docket / "10_decision_memo.md").exists():
        memo = (docket / "10_decision_memo.md").read_text(encoding="utf-8")
        if "PASSED" not in memo:
            warnings.append("decision memo does not contain PASSED")
        if "Claim boundary" not in memo and "claim boundary" not in memo:
            warnings.append("decision memo does not include an explicit claim boundary")
    return {
        "schema": "agialpha.docket_lint.v1",
        "status": "pass" if not errors else "fail",
        "strict": strict,
        "errors": errors,
        "warnings": warnings,
        "base_required_files": BASE_REQUIRED,
        "publication_required_files": PUBLICATION_REQUIRED,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def compute_hash_manifest(docket: Path) -> dict[str, Any]:
    files = []
    for p in sorted(docket.iterdir()):
        if p.is_file() and p.name != "15_hash_manifest.json":
            files.append({"path": p.name, "sha256": sha256_file(p), "bytes": p.stat().st_size})
    return {
        "schema": "agialpha.hash_manifest.v1",
        "generated_at_epoch": now_epoch(),
        "root_sha256": sha256_bytes(canonical_json_bytes(files)),
        "files": files,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ensure_base_docket(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    data_dir = Path(__file__).resolve().parents[1] / "evidence-docket"
    if data_dir.exists():
        for p in data_dir.iterdir():
            if p.is_file() and not (out / p.name).exists():
                shutil.copy2(p, out / p.name)
        return
    write_json(out / "00_manifest.json", {
        "schema": "agialpha.evidence_docket_manifest.v1",
        "docket_id": "fallback-evidence-docket",
        "claim_boundary": CLAIM_BOUNDARY,
        "status": "fallback_scaffold"
    })
    for name in BASE_REQUIRED:
        p = out / name
        if p.exists():
            continue
        if name.endswith(".json"):
            write_json(p, {"schema": f"agialpha.{name}.fallback", "claim_boundary": CLAIM_BOUNDARY})
        else:
            p.write_text("# Fallback Evidence Docket\n\nClaim boundary: fallback scaffold only.\n", encoding="utf-8")


def make_cost_ledger(docket: Path) -> dict[str, Any]:
    return {
        "schema": "agialpha.cost_ledger.v1",
        "generated_at_epoch": now_epoch(),
        "tokens": int(os.environ.get("AGIALPHA_TOKENS", "0") or 0),
        "api_cost_usd": float(os.environ.get("AGIALPHA_API_COST_USD", "0") or 0),
        "tool_calls": int(os.environ.get("AGIALPHA_TOOL_CALLS", "0") or 0),
        "ci_runtime_seconds": float(os.environ.get("AGIALPHA_CI_RUNTIME_SECONDS", "0") or 0),
        "wall_seconds": float(os.environ.get("AGIALPHA_WALL_SECONDS", "0") or 0),
        "human_review_minutes": float(os.environ.get("AGIALPHA_HUMAN_REVIEW_MINUTES", "0") or 0),
        "github_run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "0"),
        "claim_boundary": "Cost ledger is scaffold-level unless model/API/tool invoices and hardware logs are attached. " + CLAIM_BOUNDARY,
    }


def _safe_list_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    value = read_json(path)
    if isinstance(value, list):
        return [x for x in value if isinstance(x, dict)]
    if isinstance(value, dict):
        for key in ["accepted_interventions", "items", "interventions"]:
            if isinstance(value.get(key), list):
                return [x for x in value[key] if isinstance(x, dict)]
    return []


def make_safety_ledger(docket: Path) -> dict[str, Any]:
    accepted = _safe_list_json(docket / "06_accepted_interventions.json")
    risk_tiers = sorted({str(x.get("risk_tier", "ALLOW")) for x in accepted}) or ["ALLOW"]
    verdicts = sorted({str(x.get("red_team_verdict", "ALLOW")) for x in accepted}) or ["ALLOW"]
    critical = any(x in {"RESTRICTED", "PROHIBITED"} for x in risk_tiers) or any(x in {"RESTRICT", "PROHIBIT"} for x in verdicts)
    return {
        "schema": "agialpha.safety_ledger.v1",
        "generated_at_epoch": now_epoch(),
        "critical_violations": int(critical),
        "blocked_actions": [],
        "risk_tiers_seen": risk_tiers,
        "red_team_verdicts": verdicts,
        "unsafe_promotion_attempts": 0,
        "claim_boundary_present": "claim_boundary" in (read_json(docket / "00_manifest.json") if (docket / "00_manifest.json").exists() else {}),
        "notes": [
            "Evidence Factory v0.3 treats this as a bounded CI evidence scaffold unless independently reviewed.",
            "No equipment control, deployment, sensitive action, or production authority is exercised by this scaffold."
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_baselines(docket: Path) -> dict[str, Any]:
    comp = read_json(docket / "09_treatment_control_comparison.json") if (docket / "09_treatment_control_comparison.json").exists() else {}
    treatment = comp.get("treatment_yield") or comp.get("treatment") or comp.get("treatment_score") or 0
    control = comp.get("control_yield") or comp.get("control") or comp.get("control_score") or 0
    try:
        advantage_delta = float(treatment) - float(control)
    except Exception:
        advantage_delta = 0.0
    return {
        "schema": "agialpha.baseline_results.v1",
        "generated_at_epoch": now_epoch(),
        "primary_metric": comp.get("primary_metric", "reuse_lift"),
        "baselines": [
            {"id": "B0_no_compiler_reuse", "status": "observed_scaffold", "score": control, "description": "Seed/control without compiler reuse."},
            {"id": "B1_manual_reuse_heuristic", "status": "pending_execution", "score": None, "description": "Manual reuse heuristic baseline."},
            {"id": "B2_single_agent_compiler_extraction", "status": "pending_execution", "score": None, "description": "Single-agent compiler extraction."},
            {"id": "B3_loop_without_MARK", "status": "pending_execution", "score": None, "description": "Deterministic loop without MARK review."},
            {"id": "B4_full_loop_MARK_Evidence_Docket", "status": "observed_scaffold", "score": treatment, "description": "Full first-loop scaffold with MARK and Evidence Docket."}
        ],
        "baseline_win_against_B0": advantage_delta > 0,
        "advantage_delta_vs_B0": round(advantage_delta, 6),
        "reuse_lift_percent_vs_B0": comp.get("reuse_lift_percent"),
        "full_baseline_suite_executed": False,
        "claim_boundary": "B0 and B4 may be represented by the current scaffold. B1-B3 must be executed for publication-grade baseline-comparative evidence. " + CLAIM_BOUNDARY,
    }


def make_replay_report(expected: Path, actual: Path | None = None) -> dict[str, Any]:
    report: dict[str, Any] = {
        "schema": "agialpha.replay_report.v1",
        "generated_at_epoch": now_epoch(),
        "status": "pending",
        "independent": False,
        "claim_boundary": "Internal CI replay is not the same as independent reviewer replication. " + CLAIM_BOUNDARY,
    }
    if actual and actual.exists():
        mismatches: list[dict[str, Any]] = []
        for name in BASE_REQUIRED:
            ep = expected / name
            ap = actual / name
            if not ap.exists():
                mismatches.append({"file": name, "error": "missing in actual replay"})
                continue
            if not ep.exists():
                continue
            if name.endswith(".json"):
                try:
                    e = read_json(ep)
                    a = read_json(ap)
                    for unstable in ["created_at", "generated_at_epoch", "timestamp"]:
                        if isinstance(e, dict): e.pop(unstable, None)
                        if isinstance(a, dict): a.pop(unstable, None)
                    if e != a:
                        mismatches.append({"file": name, "error": "json mismatch"})
                except Exception as exc:
                    mismatches.append({"file": name, "error": f"json compare error: {exc}"})
            else:
                if ep.read_text(encoding="utf-8") != ap.read_text(encoding="utf-8"):
                    mismatches.append({"file": name, "error": "text mismatch"})
        report.update({
            "status": "pass" if not mismatches else "fail",
            "mismatches": mismatches,
            "expected_root_sha256": compute_hash_manifest(expected)["root_sha256"],
            "actual_root_sha256": compute_hash_manifest(actual)["root_sha256"],
        })
    return report


def make_independent_review(docket: Path) -> str:
    return """# Independent Review

Status: pending independent reviewer replay.

Reviewer: TBD

Required review steps:

1. Clone a fresh repository or fork.
2. Pin the source commit from `18_source_snapshot.json`.
3. Run `REPLAY_INSTRUCTIONS.md` without hidden manual steps.
4. Confirm `14_replay_report.json`.
5. Confirm cost and safety ledgers.
6. Confirm baseline status.
7. Sign this file with reviewer identity and date.

Claim boundary: this file is intentionally pending until completed by an independent reviewer.
"""


def make_state_for_next_run(docket: Path) -> dict[str, Any]:
    manifest = read_json(docket / "00_manifest.json") if (docket / "00_manifest.json").exists() else {}
    previous_cycle = 0
    existing_state = docket / "17_state_for_next_run.json"
    if existing_state.exists():
        try:
            previous_cycle = int(read_json(existing_state).get("state_manifest", {}).get("cycle_index", 0))
        except Exception:
            previous_cycle = 0
    accepted = _safe_list_json(docket / "06_accepted_interventions.json")
    compiler_present = (docket / "07_coldchain_energy_compiler_v0.json").exists()
    return {
        "schema": "agialpha.rsi_state_for_next_run.v1",
        "state_manifest": {
            "cycle_index": previous_cycle + 1,
            "previous_docket_id": manifest.get("docket_id", "unknown"),
            "state_payload_hash_pending": True,
            "persistence_rule": "cycle_index increments exactly +1; archive counters must not silently reset."
        },
        "archive": {
            "frontier_cells": max(1, int(os.environ.get("AGIALPHA_FRONTIER_CELLS", "1") or 1)),
            "candidates": max(2, len(accepted) + 1),
            "occupied_cells": 1 if compiler_present else 0,
            "artifacts": ["ColdChain-Energy-Compiler-v0"] if compiler_present else [],
        },
        "eci": {
            "ledger_total": 1,
            "highest_evidence_level": "E2_EXECUTED_SCAFFOLD"
        },
        "next_action": "Run clean replay, full baseline suite, cost/safety audit, and independent review.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_claim_boundary() -> dict[str, Any]:
    return {
        "schema": "agialpha.claim_boundary.v1",
        "boundary": CLAIM_BOUNDARY,
        "forbidden_claims": [
            "achieved AGI",
            "achieved ASI",
            "empirical SOTA without baselines",
            "safe autonomy without adversarial evidence",
            "guaranteed economic return",
            "civilization-scale capability"
        ],
        "required_for_stronger_claims": [
            "independent replay",
            "full baseline suite",
            "cost ledger review",
            "safety ledger review",
            "delayed outcome or external validation"
        ]
    }


def make_claim_level(docket: Path) -> dict[str, Any]:
    lint = lint_docket(docket, strict=False)
    base_ok = lint["status"] == "pass"
    replay = read_json(docket / "14_replay_report.json") if (docket / "14_replay_report.json").exists() else {}
    safety = read_json(docket / "12_safety_ledger.json") if (docket / "12_safety_ledger.json").exists() else {}
    baselines = read_json(docket / "13_baseline_results.json") if (docket / "13_baseline_results.json").exists() else {}
    review = (docket / "16_independent_review.md").read_text(encoding="utf-8") if (docket / "16_independent_review.md").exists() else ""
    level = "L1"
    reasons = []
    if base_ok:
        level = "L3"
        reasons.append("base Evidence Docket files present")
    if replay.get("status") == "pass":
        level = "L3.5"
        reasons.append("internal clean-CI replay report passed")
    independent_pass = ("Status: passed" in review or "Status: PASSED" in review or os.environ.get("INDEPENDENT_REVIEW_PASSED") == "true")
    if independent_pass and replay.get("status") == "pass":
        level = "L4"
        reasons.append("independent review marked passed")
    full_baselines = bool(baselines.get("full_baseline_suite_executed"))
    if level in {"L4", "L3.5"} and full_baselines and safety.get("critical_violations", 1) == 0 and baselines.get("baseline_win_against_B0"):
        level = "L5"
        reasons.append("full baseline suite executed and AGI ALPHA won with clean safety ledger")
    return {
        "schema": "agialpha.claim_level.v1",
        "generated_at_epoch": now_epoch(),
        "current_level": level,
        "levels": CLAIM_LEVELS,
        "promotion_reasons": reasons,
        "claim_boundary": "Claim level is deliberately conservative. " + CLAIM_BOUNDARY,
    }


def complete_docket(docket: Path, out: Path | None = None, actual_replay: Path | None = None) -> Path:
    if out:
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(docket, out)
        docket = out
    ensure_base_docket(docket)
    write_json(docket / "11_cost_ledger.json", make_cost_ledger(docket))
    write_json(docket / "12_safety_ledger.json", make_safety_ledger(docket))
    write_json(docket / "13_baseline_results.json", make_baselines(docket))
    write_json(docket / "14_replay_report.json", make_replay_report(docket, actual_replay))
    write_json(docket / "18_source_snapshot.json", source_snapshot(Path.cwd()))
    write_json(docket / "19_claim_boundary.json", make_claim_boundary())
    if not (docket / "16_independent_review.md").exists():
        (docket / "16_independent_review.md").write_text(make_independent_review(docket), encoding="utf-8")
    write_json(docket / "17_state_for_next_run.json", make_state_for_next_run(docket))
    write_json(docket / "15_hash_manifest.json", compute_hash_manifest(docket))
    write_json(docket / "claim_level.json", make_claim_level(docket))
    write_json(docket / "15_hash_manifest.json", compute_hash_manifest(docket))
    return docket


def copy_or_seed_docket(source: Path | None, out: Path) -> Path:
    if out.exists():
        shutil.rmtree(out)
    if source and source.exists():
        shutil.copytree(source, out)
    else:
        out.mkdir(parents=True, exist_ok=True)
        ensure_base_docket(out)
    return out


def seed_matrix(base: Path, out: Path, count: int = 10) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(1, count + 1):
        target = out / f"seed-{i:03d}"
        copy_or_seed_docket(base, target)
        manifest_path = target / "00_manifest.json"
        manifest = read_json(manifest_path)
        manifest["docket_id"] = f"{manifest.get('docket_id', 'evidence-docket')}-seed-{i:03d}"
        manifest["matrix_seed_index"] = i
        manifest["claim_boundary"] = CLAIM_BOUNDARY
        write_json(manifest_path, manifest)
        complete_docket(target, None, None)
        claim = read_json(target / "claim_level.json")
        comp = read_json(target / "09_treatment_control_comparison.json") if (target / "09_treatment_control_comparison.json").exists() else {}
        rows.append({"seed": i, "docket": str(target), "claim_level": claim["current_level"], "reuse_lift_percent": comp.get("reuse_lift_percent")})
    result = {"schema": "agialpha.seed_matrix.v1", "count": count, "rows": rows, "claim_boundary": CLAIM_BOUNDARY}
    write_json(out / "seed_matrix_summary.json", result)
    return result


def scaling_curve(out: Path, agent_counts: Iterable[int] = (1,2,4,8,16), node_counts: Iterable[int] = (1,2,4,8), routers: Iterable[str] = ("R0", "R1", "R2", "R5")) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for a in agent_counts:
        for n in node_counts:
            for r in routers:
                overhead = round(0.05 * max(0, a - 1) + 0.03 * max(0, n - 1), 4)
                rows.append({
                    "agents": a,
                    "nodes": n,
                    "router": r,
                    "verified_work_proxy": round((1 + 0.32 * (a ** 0.5) + 0.18 * (n ** 0.5)) / (1 + overhead), 4),
                    "coordination_overhead_proxy": overhead,
                    "status": "proxy_only_pending_real_task_measurement"
                })
    result = {"schema": "agialpha.coordination_scaling_proxy.v1", "rows": rows, "claim_boundary": "Proxy only. Scaling claims require real-task Evidence Dockets. " + CLAIM_BOUNDARY}
    write_json(out / "coordination_scaling_proxy.json", result)
    return result


def _row_from_docket(docket: Path) -> dict[str, Any] | None:
    if not docket.exists() or not (docket / "00_manifest.json").exists():
        return None
    manifest = read_json(docket / "00_manifest.json")
    claim = read_json(docket / "claim_level.json") if (docket / "claim_level.json").exists() else {"current_level": "unknown"}
    comp = read_json(docket / "09_treatment_control_comparison.json") if (docket / "09_treatment_control_comparison.json").exists() else {}
    safety = read_json(docket / "12_safety_ledger.json") if (docket / "12_safety_ledger.json").exists() else {}
    replay = read_json(docket / "14_replay_report.json") if (docket / "14_replay_report.json").exists() else {}
    baselines = read_json(docket / "13_baseline_results.json") if (docket / "13_baseline_results.json").exists() else {}
    h = read_json(docket / "15_hash_manifest.json") if (docket / "15_hash_manifest.json").exists() else {}
    return {
        "run_id": manifest.get("docket_id", docket.name),
        "path": str(docket),
        "claim_level": claim.get("current_level", "unknown"),
        "replay_status": replay.get("status", "pending"),
        "baseline_win_against_B0": baselines.get("baseline_win_against_B0", "pending"),
        "full_baseline_suite_executed": baselines.get("full_baseline_suite_executed", False),
        "reuse_lift_percent": comp.get("reuse_lift_percent"),
        "critical_safety_violations": safety.get("critical_violations", "pending"),
        "root_sha256": h.get("root_sha256"),
    }


def build_scoreboard(dockets: list[Path], out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    seen = set()
    for d in dockets:
        if d.is_file() and d.name == "00_manifest.json":
            d = d.parent
        if not d.is_dir():
            continue
        key = str(d.resolve())
        if key in seen:
            continue
        seen.add(key)
        row = _row_from_docket(d)
        if row:
            rows.append(row)
    rows = sorted(rows, key=lambda r: (str(r.get("run_id")), str(r.get("path"))))
    index = {"schema": "agialpha.evidence_scoreboard.v1", "generated_at_epoch": now_epoch(), "claim_boundary": CLAIM_BOUNDARY, "runs": rows}
    write_json(out / "evidence-index.json", index)
    html = [
        "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
        "<title>AGI ALPHA Evidence Factory Scoreboard</title>",
        "<style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;margin:2rem;line-height:1.45;color:#172033;background:#fbfbfd}h1{letter-spacing:.02em}.box{background:#fff;border:1px solid #ddd;border-radius:12px;padding:1rem;margin:1rem 0}table{border-collapse:collapse;width:100%;background:#fff}td,th{border:1px solid #e1e4e8;padding:.55rem;text-align:left;vertical-align:top}th{background:#f3f5f8}.pass{color:#087a2e;font-weight:700}.pending{color:#8a6100;font-weight:700}.fail{color:#b42318;font-weight:700}code{background:#f2f2f2;padding:.15rem .3rem;border-radius:4px}</style></head><body>",
        "<h1>AGI ALPHA Evidence Factory Scoreboard</h1>",
        f"<div class='box'><strong>Claim boundary:</strong> {CLAIM_BOUNDARY}</div>",
        "<table><thead><tr><th>Run</th><th>Claim level</th><th>Replay</th><th>Baseline win</th><th>Full baselines?</th><th>Reuse lift</th><th>Safety incidents</th><th>Root hash</th><th>Path</th></tr></thead><tbody>"
    ]
    for r in rows:
        replay_class = "pass" if r["replay_status"] == "pass" else ("fail" if r["replay_status"] == "fail" else "pending")
        html.append("<tr>" + "".join([
            f"<td>{r['run_id']}</td>",
            f"<td><code>{r['claim_level']}</code></td>",
            f"<td class='{replay_class}'>{r['replay_status']}</td>",
            f"<td>{r['baseline_win_against_B0']}</td>",
            f"<td>{r['full_baseline_suite_executed']}</td>",
            f"<td>{r['reuse_lift_percent']}</td>",
            f"<td>{r['critical_safety_violations']}</td>",
            f"<td><code>{(r.get('root_sha256') or '')[:16]}</code></td>",
            f"<td><code>{r['path']}</code></td>",
        ]) + "</tr>")
    html.append("</tbody></table><p>No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.</p></body></html>")
    (out / "scoreboard.html").write_text("\n".join(html), encoding="utf-8")
    (out / "index.html").write_text("\n".join(html), encoding="utf-8")
    return index


def next_seed_payload(docket: Path) -> dict[str, Any]:
    manifest = read_json(docket / "00_manifest.json") if (docket / "00_manifest.json").exists() else {}
    claim = read_json(docket / "claim_level.json") if (docket / "claim_level.json").exists() else {"current_level": "unknown"}
    comp = read_json(docket / "09_treatment_control_comparison.json") if (docket / "09_treatment_control_comparison.json").exists() else {}
    return {
        "schema": "agialpha.next_seed_proposal.v1",
        "created_at_epoch": now_epoch(),
        "parent_docket_id": manifest.get("docket_id", docket.name),
        "parent_claim_level": claim.get("current_level"),
        "observed_reuse_lift_percent": comp.get("reuse_lift_percent"),
        "proposal": {
            "action": "run_next_seed_matrix_and_full_baselines",
            "required_gates": ["cost_ledger", "safety_ledger", "baseline_suite", "clean_replay", "independent_review"],
            "claim_boundary": CLAIM_BOUNDARY
        }
    }
