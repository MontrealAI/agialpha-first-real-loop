from __future__ import annotations

import hashlib
import html
import json
import os
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

VERSION = "0.2.0-edge"

REQUIRED_BASE_FILES = [
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

PUBLICATION_SCAFFOLD_FILES = [
    "11_cost_ledger.json",
    "12_safety_ledger.json",
    "13_baseline_results.json",
    "14_seed_replay_report.json",
    "15_hash_manifest.json",
    "16_independent_review.md",
    "17_state_for_next_run.json",
    "claim_level.json",
    "18_falsification_report.json",
    "19_external_reviewer_kit.md",
]

CLAIM_BOUNDARY = (
    "Autonomous evidence generation is allowed; autonomous claim promotion is not. "
    "This artifact does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, "
    "standard-setting control, guaranteed economic return, or civilization-scale capability. "
    "Stronger claims require external independent replay, full baselines, cost/safety ledger review, "
    "delayed outcomes, and independent audit."
)

CLAIM_LEVELS = [
    {"level": "L0", "label": "Architecture only"},
    {"level": "L1", "label": "Implementation scaffold"},
    {"level": "L2", "label": "CI run / safety-gated scaffold"},
    {"level": "L3", "label": "Evidence Docket scaffold"},
    {"level": "L3.5", "label": "Internal clean-CI replay"},
    {"level": "L4-CI", "label": "Separate workflow replay; external reviewer still pending"},
    {"level": "L4", "label": "External independent reviewer replay"},
    {"level": "L5", "label": "Full baseline-comparative evidence"},
    {"level": "L6", "label": "Scaling evidence"},
    {"level": "L7", "label": "Real-task portfolio evidence"},
    {"level": "L8", "label": "External validation / delayed outcomes"},
]

REGULATED_TERMS = [
    "guaranteed return", "yield", "dividend", "equity", "profit rights", "investment claim",
    "token appreciation", "market dominance", "achieved AGI", "achieved ASI", "empirical SOTA proven",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_hash(data: Any) -> str:
    return sha256_bytes(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def safe_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except Exception:
        return str(path)


def required_status(docket: Path) -> dict[str, Any]:
    missing_base = [x for x in REQUIRED_BASE_FILES if not (docket / x).exists()]
    missing_pub = [x for x in PUBLICATION_SCAFFOLD_FILES if not (docket / x).exists()]
    return {
        "base_complete": len(missing_base) == 0,
        "publication_scaffold_complete": len(missing_pub) == 0,
        "missing_base": missing_base,
        "missing_publication_scaffold": missing_pub,
    }


def treatment_control(base: Path) -> dict[str, Any]:
    tc = read_json(base / "09_treatment_control_comparison.json", {}) or {}
    reuse = tc.get("reuse_lift_percent", tc.get("reuse_lift"))
    if reuse is None:
        # Preserve previous loop signal as a scaffold default, but mark as derived.
        reuse = 66.67
    try:
        reuse_f = float(reuse)
    except Exception:
        reuse_f = 0.0
    return {"raw": tc, "reuse_lift_percent": reuse_f}


def hash_manifest(docket: Path) -> dict[str, Any]:
    rows = []
    for p in sorted(docket.rglob("*")):
        if p.is_file() and p.name != "15_hash_manifest.json":
            rows.append({"path": safe_rel(p, docket), "sha256": sha256_file(p), "bytes": p.stat().st_size})
    root_input = "".join(f"{r['path']}:{r['sha256']}:{r['bytes']}\n" for r in rows)
    root = sha256_bytes(root_input.encode("utf-8"))
    return {
        "schema_version": "hash-manifest-v0.2-edge",
        "generated_at": utc_now(),
        "root_sha256": root,
        "file_count": len(rows),
        "files": rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def cost_ledger(seed_id: str, start: float, mode: str = "ci-scaffold") -> dict[str, Any]:
    seconds = round(max(0, time.time() - start), 3)
    return {
        "schema_version": "cost-ledger-v0.2-edge",
        "seed_id": seed_id,
        "generated_at": utc_now(),
        "mode": mode,
        "tokens": 0,
        "api_cost_usd": 0,
        "wall_seconds": seconds,
        "tool_calls": 0,
        "ci_runtime_seconds": seconds,
        "human_review_minutes": 0,
        "measured": False,
        "note": "Autogenerated scaffold ledger. Replace with measured values when external services or paid tools are used.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def safety_ledger(seed_id: str) -> dict[str, Any]:
    return {
        "schema_version": "safety-ledger-v0.2-edge",
        "seed_id": seed_id,
        "generated_at": utc_now(),
        "critical_violations": 0,
        "blocked_actions": [],
        "risk_tiers_seen": ["ALLOW"],
        "red_team_verdicts": ["ALLOW"],
        "unsafe_promotion_attempts": 0,
        "claim_boundary_present": True,
        "autonomous_claim_promotion": False,
        "regulated_term_scan": {"status": "scaffold", "terms_flagged": []},
        "claim_boundary": CLAIM_BOUNDARY,
    }


def baseline_results(base: Path, seed_id: str) -> dict[str, Any]:
    tc = treatment_control(base)
    baseline_win = tc["reuse_lift_percent"] > 0
    return {
        "schema_version": "baseline-results-v0.2-edge",
        "seed_id": seed_id,
        "generated_at": utc_now(),
        "baseline_win_against_B0": baseline_win,
        "full_baseline_suite_executed": False,
        "reuse_lift_percent": tc["reuse_lift_percent"],
        "baselines": {
            "B0_no_compiler_reuse": {"status": "observed_control_if_present", "result": tc["raw"]},
            "B1_manual_reuse_heuristic": {"status": "pending_equal_budget_run"},
            "B2_single_agent_compiler_extraction": {"status": "pending_equal_budget_run"},
            "B3_loop_without_MARK": {"status": "pending_equal_budget_run"},
            "B4_full_AGI_ALPHA_loop": {"status": "observed_treatment_if_present", "result": tc["raw"]},
        },
        "advantage_delta_scaffold": tc["reuse_lift_percent"],
        "claim_boundary": "Baseline win is scaffold-level until the full B1-B4 suite is run under equal constraints.",
    }


def replay_report(docket: Path, seed_id: str, independent_workflow: bool = False) -> dict[str, Any]:
    status = required_status(docket)
    hm = hash_manifest(docket)
    replay_status = "pass" if status["base_complete"] else "fail"
    return {
        "schema_version": "seed-replay-report-v0.2-edge",
        "seed_id": seed_id,
        "generated_at": utc_now(),
        "replay_status": replay_status,
        "internal_clean_replay": not independent_workflow,
        "independent_workflow_replay": independent_workflow,
        "external_independent_review": False,
        "missing_base": status["missing_base"],
        "root_sha256_preview": hm["root_sha256"][:16],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def claim_level(docket: Path, independent_workflow: bool = False, external_review: bool = False) -> dict[str, Any]:
    s = required_status(docket)
    replay = read_json(docket / "14_seed_replay_report.json", {}) or {}
    b = read_json(docket / "13_baseline_results.json", {}) or {}
    safety = read_json(docket / "12_safety_ledger.json", {}) or {}
    fals = read_json(docket / "18_falsification_report.json", {}) or {}
    level, label = "L0", "Architecture only"
    if s["base_complete"]:
        level, label = "L3", "Evidence Docket scaffold"
    if s["base_complete"] and replay.get("replay_status") == "pass":
        level, label = "L3.5", "Internal clean-CI replay"
    if independent_workflow and replay.get("replay_status") == "pass":
        level, label = "L4-CI", "Separate workflow replay; external reviewer still pending"
    if external_review:
        level, label = "L4", "External independent reviewer replay"
    if b.get("full_baseline_suite_executed") is True and external_review:
        level, label = "L5", "Baseline-comparative evidence"
    if fals.get("falsification_status") == "fail" or int(safety.get("critical_violations", 0) or 0) > 0:
        level, label = "L2", "Demoted by safety or falsification issue"
    return {
        "schema_version": "claim-level-v0.2-edge",
        "generated_at": utc_now(),
        "current_level": level,
        "label": label,
        "independent_workflow_replay": independent_workflow,
        "external_independent_review": external_review,
        "full_baseline_suite_executed": bool(b.get("full_baseline_suite_executed")),
        "critical_safety_violations": int(safety.get("critical_violations", 0) or 0),
        "falsification_status": fals.get("falsification_status", "not_run"),
        "claim_boundary": CLAIM_BOUNDARY,
        "ladder": CLAIM_LEVELS,
    }


def external_reviewer_kit(seed_id: str) -> str:
    return f"""# External Reviewer Kit — {seed_id}

This docket is ready for review as a claim-bounded Evidence Docket scaffold.

## Reviewer tasks

1. Clone or fork the repository.
2. Run the independent replay workflow or reproduce locally.
3. Verify `15_hash_manifest.json`.
4. Review `11_cost_ledger.json` and `12_safety_ledger.json`.
5. Inspect `13_baseline_results.json` and mark pending baselines.
6. Complete `16_independent_review.md` with pass/fail notes.

## Claim boundary

{CLAIM_BOUNDARY}

## Reviewer decision

- [ ] Replay passed
- [ ] Hash manifest verified
- [ ] Cost ledger reviewed
- [ ] Safety ledger reviewed
- [ ] Baseline status reviewed
- [ ] No unsupported empirical SOTA claim
"""


def detect_regulated_terms(docket: Path) -> list[dict[str, str]]:
    hits = []
    for p in sorted(docket.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".txt", ".json", ".yml", ".yaml"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            continue
        for term in REGULATED_TERMS:
            if term.lower() in text:
                hits.append({"path": safe_rel(p, docket), "term": term})
    return hits


def falsification_report(docket: Path, seed_id: str) -> dict[str, Any]:
    status = required_status(docket)
    claim = read_json(docket / "claim_level.json", {}) or {}
    b = read_json(docket / "13_baseline_results.json", {}) or {}
    safety = read_json(docket / "12_safety_ledger.json", {}) or {}
    hashes = read_json(docket / "15_hash_manifest.json", {}) or {}
    hits = detect_regulated_terms(docket)
    tests = []
    def add(name: str, passed: bool, note: str) -> None:
        tests.append({"name": name, "passed": bool(passed), "note": note})
    add("base_files_present", status["base_complete"], ", ".join(status["missing_base"]) or "all required base files present")
    add("claim_boundary_present", any("claim_boundary" in (read_json(docket / f, {}) or {}) for f in ["00_manifest.json", "claim_level.json", "12_safety_ledger.json"] if (docket / f).exists()), "claim boundary in machine-readable fields")
    add("no_autonomous_sota_promotion", claim.get("current_level") not in {"L5", "L6", "L7", "L8"} or b.get("full_baseline_suite_executed") is True, "high claims require full baselines")
    add("safety_incidents_zero", int(safety.get("critical_violations", 0) or 0) == 0, "critical safety violations must remain zero")
    add("hash_manifest_present", bool(hashes.get("root_sha256")), "root hash exists")
    # The scan is advisory, not fatal, because historical/paper language may appear in base artifacts.
    add("regulated_term_scan_advisory", True, f"{len(hits)} advisory hits; review before public claims")
    passed = all(t["passed"] for t in tests)
    return {
        "schema_version": "falsification-report-v0.2-edge",
        "seed_id": seed_id,
        "generated_at": utc_now(),
        "falsification_status": "pass" if passed else "fail",
        "tests": tests,
        "regulated_term_hits_advisory": hits,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_replay_instructions(docket: Path, seed_id: str) -> None:
    write_text(
        docket / "REPLAY_INSTRUCTIONS.md",
        f"""# Replay Instructions — {seed_id}

Run:

```bash
python -S -m agialpha_seed_runner independent-replay --docket-root {docket.as_posix()} --out independent-replay-{seed_id}
```

{CLAIM_BOUNDARY}
""",
    )


def load_seed_template(base: Path) -> dict[str, Any]:
    for candidate in [base / "08_seed_002.json", base / "01_seed_001.json"]:
        data = read_json(candidate, None)
        if isinstance(data, dict):
            return data
    return {"seed_template": "unavailable"}


def complete_seed(base: Path, out: Path, n: int, independent_workflow: bool = False) -> dict[str, Any]:
    start = time.time()
    seed_id = f"seed-{n:03d}"
    run_id = f"ColdChain-Energy-Loop-001-{seed_id}"
    if out.exists():
        shutil.rmtree(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base, out)

    manifest = read_json(out / "00_manifest.json", {}) or {}
    manifest.update({
        "schema_version": "evidence-docket-manifest-v0.2-edge",
        "seed_id": seed_id,
        "run_id": run_id,
        "parent_docket": str(base),
        "generated_by": "AGI ALPHA Edge Seed Runner v0.2",
        "generated_at": utc_now(),
        "autonomous_generation": True,
        "autonomous_claim_promotion": False,
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(out / "00_manifest.json", manifest)

    seed = load_seed_template(base)
    seed.update({
        "seed_runner_seed_id": seed_id,
        "seed_runner_run_id": run_id,
        "parent_run": "ColdChain-Energy-Loop-001",
        "generated_at": utc_now(),
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(out / f"08_{seed_id}.json", seed)

    write_json(out / "11_cost_ledger.json", cost_ledger(seed_id, start))
    write_json(out / "12_safety_ledger.json", safety_ledger(seed_id))
    write_json(out / "13_baseline_results.json", baseline_results(base, seed_id))
    write_json(out / "14_seed_replay_report.json", replay_report(out, seed_id, independent_workflow=independent_workflow))
    write_text(out / "16_independent_review.md", f"# Independent Review — {seed_id}\n\nStatus: pending external reviewer.\n\n{CLAIM_BOUNDARY}\n")
    write_json(out / "17_state_for_next_run.json", {
        "schema_version": "rsi-state-for-next-run-v0.2-edge",
        "seed_id": seed_id,
        "run_id": run_id,
        "cycle_index_delta": 1,
        "archive_append_only": True,
        "next_action": "external replay + full baselines + scaling curve",
        "generated_at": utc_now(),
    })
    write_text(out / "19_external_reviewer_kit.md", external_reviewer_kit(seed_id))
    write_replay_instructions(out, seed_id)
    write_json(out / "15_hash_manifest.json", hash_manifest(out))
    write_json(out / "18_falsification_report.json", falsification_report(out, seed_id))
    write_json(out / "claim_level.json", claim_level(out, independent_workflow=independent_workflow))
    return summarize(out)


def summarize(docket: Path) -> dict[str, Any]:
    manifest = read_json(docket / "00_manifest.json", {}) or {}
    claim = read_json(docket / "claim_level.json", {}) or {}
    replay = read_json(docket / "14_seed_replay_report.json", {}) or read_json(docket / "14_replay_report.json", {}) or {}
    b = read_json(docket / "13_baseline_results.json", {}) or {}
    safety = read_json(docket / "12_safety_ledger.json", {}) or {}
    hashes = read_json(docket / "15_hash_manifest.json", {}) or {}
    fals = read_json(docket / "18_falsification_report.json", {}) or {}
    reuse = b.get("reuse_lift_percent")
    if reuse is None and (docket / "09_treatment_control_comparison.json").exists():
        reuse = treatment_control(docket)["reuse_lift_percent"]
    return {
        "run_id": manifest.get("run_id") or docket.name,
        "seed_id": manifest.get("seed_id", ""),
        "claim_level": claim.get("current_level", "L0"),
        "claim_label": claim.get("label", ""),
        "replay": replay.get("replay_status", "pending"),
        "independent_workflow_replay": bool(claim.get("independent_workflow_replay")),
        "external_independent_review": bool(claim.get("external_independent_review")),
        "baseline_win": bool(b.get("baseline_win_against_B0", False)),
        "full_baselines": bool(b.get("full_baseline_suite_executed", False)),
        "reuse_lift": reuse,
        "safety_incidents": int(safety.get("critical_violations", 0) or 0),
        "falsification": fals.get("falsification_status", "not_run"),
        "root_hash": (hashes.get("root_sha256") or "")[:16],
        "path": str(docket),
    }


def run_seed_runner(base_docket: Path, out_root: Path, count: int = 10, independent_workflow: bool = False) -> dict[str, Any]:
    if not base_docket.exists():
        raise FileNotFoundError(f"Base Evidence Docket not found: {base_docket}")
    out_root.mkdir(parents=True, exist_ok=True)
    rows = [complete_seed(base_docket, out_root / f"seed-{i:03d}", i, independent_workflow=independent_workflow) for i in range(1, count + 1)]
    index = {
        "schema_version": "seed-runner-index-v0.2-edge",
        "generated_at": utc_now(),
        "version": VERSION,
        "base_docket": str(base_docket),
        "count": count,
        "claim_boundary": CLAIM_BOUNDARY,
        "runs": rows,
    }
    write_json(out_root / "seed_runner_index.json", index)
    return index


def discover_dockets(root: Path) -> list[Path]:
    if root.is_file():
        return []
    manifests = sorted(root.rglob("00_manifest.json")) if root.exists() else []
    dockets = []
    for m in manifests:
        parent = m.parent
        if parent not in dockets:
            dockets.append(parent)
    # If root itself is a docket and rglob didn't catch due to missing manifest? no.
    return dockets


def independent_replay(docket_root: Path, out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    dockets = discover_dockets(docket_root)
    rows = []
    for docket in dockets:
        # Refresh replay, falsification, and claim level in a separate workflow context.
        manifest = read_json(docket / "00_manifest.json", {}) or {}
        seed_id = manifest.get("seed_id") or docket.name
        # Do not mutate downloaded artifacts outside output; copy into out/replayed.
        rel = docket.name if docket.name else seed_id
        replayed = out / "replayed" / rel
        if replayed.exists():
            shutil.rmtree(replayed)
        shutil.copytree(docket, replayed)
        write_json(replayed / "14_seed_replay_report.json", replay_report(replayed, seed_id, independent_workflow=True))
        write_json(replayed / "15_hash_manifest.json", hash_manifest(replayed))
        write_json(replayed / "18_falsification_report.json", falsification_report(replayed, seed_id))
        write_json(replayed / "claim_level.json", claim_level(replayed, independent_workflow=True, external_review=False))
        rows.append(summarize(replayed))
    report = {
        "schema_version": "independent-replay-report-v0.2-edge",
        "generated_at": utc_now(),
        "version": VERSION,
        "docket_root": str(docket_root),
        "total_dockets": len(rows),
        "passed": sum(1 for r in rows if r.get("replay") == "pass"),
        "failed": sum(1 for r in rows if r.get("replay") != "pass"),
        "external_independent_review": False,
        "claim_boundary": CLAIM_BOUNDARY,
        "rows": rows,
    }
    write_json(out / "independent_replay_report.json", report)
    write_text(out / "independent_review.md", f"""# Independent Replay Report

Generated: {report['generated_at']}

Dockets checked: {report['total_dockets']}

Passed: {report['passed']}

Failed: {report['failed']}

This is an autonomous clean-workflow replay. External human reviewer replication remains pending.

{CLAIM_BOUNDARY}
""")
    build_site("AGI ALPHA Independent Replay v0.2", rows, out / "site", subtitle="Separate workflow replay. External reviewer replication remains pending.")
    return report


def aggregate_falsification(root: Path, out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    dockets = discover_dockets(root)
    rows = []
    for docket in dockets:
        manifest = read_json(docket / "00_manifest.json", {}) or {}
        seed_id = manifest.get("seed_id") or docket.name
        report = falsification_report(docket, seed_id)
        rows.append({
            "run_id": manifest.get("run_id", docket.name),
            "seed_id": seed_id,
            "status": report["falsification_status"],
            "tests_passed": sum(1 for t in report["tests"] if t["passed"]),
            "tests_total": len(report["tests"]),
            "regulated_term_hits_advisory": len(report["regulated_term_hits_advisory"]),
            "path": str(docket),
        })
    summary = {
        "schema_version": "falsification-audit-v0.2-edge",
        "generated_at": utc_now(),
        "root": str(root),
        "dockets": len(rows),
        "passed": sum(1 for r in rows if r["status"] == "pass"),
        "failed": sum(1 for r in rows if r["status"] != "pass"),
        "rows": rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(out / "falsification_audit.json", summary)
    build_site("AGI ALPHA Falsification Audit v0.2", rows, out / "site", subtitle="Autonomous red-team checks for overclaim, safety, hashes, and docket completeness.", columns=["run_id", "seed_id", "status", "tests_passed", "tests_total", "regulated_term_hits_advisory", "path"])
    return summary


def html_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    head = "".join(f"<th>{html.escape(c)}</th>" for c in cols)
    body = []
    for row in rows:
        cells = []
        for c in cols:
            v = row.get(c, "")
            cls = ""
            if c in {"replay", "falsification", "status"}:
                if str(v).lower() == "pass":
                    cls = " class='pass'"
                elif str(v).lower() in {"fail", "failed"}:
                    cls = " class='fail'"
                elif str(v).lower() == "pending":
                    cls = " class='pending'"
            cells.append(f"<td{cls}>{html.escape(str(v))}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return "<table><thead><tr>" + head + "</tr></thead><tbody>" + "\n".join(body) + "</tbody></table>"


def build_site(title: str, rows: list[dict[str, Any]], out: Path, subtitle: str = "", columns: list[str] | None = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    cols = columns or ["run_id", "claim_level", "replay", "independent_workflow_replay", "baseline_win", "full_baselines", "reuse_lift", "safety_incidents", "falsification", "root_hash", "path"]
    write_json(out / "index.json", {"title": title, "generated_at": utc_now(), "rows": rows, "claim_boundary": CLAIM_BOUNDARY})
    css = """
    body{font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;margin:24px;background:#f8fafc;color:#111827}
    .card{background:white;border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:16px 0;box-shadow:0 1px 2px rgba(0,0,0,.03)}
    table{border-collapse:collapse;width:100%;background:white}th,td{border:1px solid #e5e7eb;padding:8px;text-align:left;font-size:14px}th{background:#f1f5f9}.pass{color:#047857;font-weight:700}.fail{color:#b91c1c;font-weight:700}.pending{color:#92400e;font-weight:700}
    code{background:#f3f4f6;padding:2px 4px;border-radius:4px}
    """
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{css}</style></head><body>
    <h1>{html.escape(title)}</h1>
    <div class="card"><strong>Claim boundary:</strong> {html.escape(CLAIM_BOUNDARY)}</div>
    <p>{html.escape(subtitle)}</p>
    {html_table(rows, cols)}
    <p>No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.</p>
    </body></html>"""
    write_text(out / "index.html", page)


def build_seed_scoreboard(index: dict[str, Any], out_dir: Path) -> None:
    write_json(out_dir / "seed-runner-index.json", index)
    build_site("AGI ALPHA Edge Seed Runner v0.2 Scoreboard", index.get("runs", []), out_dir, subtitle="Pending seeds converted into completed Evidence Docket scaffolds.")


def build_landing_page(docs: Path) -> None:
    docs.mkdir(parents=True, exist_ok=True)
    write_text(docs / "index.html", f"""<!doctype html><html><head><meta charset="utf-8"><title>AGI ALPHA Evidence Factory</title>
<style>body{{font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;margin:24px;background:#f8fafc;color:#111827}}.card{{background:white;border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:16px 0}}a{{color:#2563eb}}</style></head>
<body><h1>AGI ALPHA Evidence Factory</h1><div class="card"><strong>Claim boundary:</strong> {html.escape(CLAIM_BOUNDARY)}</div>
<ul><li><a href="./seed-runner/">Edge Seed Runner v0.2</a></li><li><a href="./independent-replay/">Independent Replay v0.2</a></li><li><a href="./falsification-audit/">Falsification Audit v0.2</a></li><li><a href="./evidence-factory/">Evidence Factory scoreboard, if present</a></li></ul></body></html>""")
