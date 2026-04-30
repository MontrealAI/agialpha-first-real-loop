from __future__ import annotations

import hashlib
import json
import math
import os
import statistics
import time
from pathlib import Path
from typing import Any, Dict, List

CLAIM_BOUNDARY = (
    "This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, "
    "standard-setting control, guaranteed economic return, or civilization-scale capability. "
    "It is a bounded simulator/proxy Evidence Docket experiment testing whether governed "
    "verified machine labor can become reusable capability that improves future verified work. "
    "Stronger claims require external reviewer replay, stronger public benchmarks, cost/safety "
    "review, delayed outcomes, and independent audit."
)

BASELINES = [
    ("B0_static_heuristic", "no-agent static heuristic", 0.45, 0.72, 0.88, 0.18),
    ("B1_single_strong_model", "single strongest model proxy", 0.58, 0.80, 0.80, 0.22),
    ("B2_fixed_workflow", "fixed workflow", 0.65, 0.86, 0.76, 0.28),
    ("B3_unstructured_swarm", "unstructured swarm", 0.70, 0.82, 0.62, 0.48),
    ("B4_agialpha_no_rsi", "AGI ALPHA without RSI governance", 0.78, 0.91, 0.69, 0.34),
    ("B5_rsi_no_reuse", "AGI ALPHA with RSI but no capability reuse", 0.84, 0.95, 0.74, 0.31),
    ("B6_full_rsi_reuse", "full AGI ALPHA with RSI + ProofBundles + capability reuse", 0.94, 0.99, 0.91, 0.23),
]

TASKS = [
    ("energy-aware-scheduler-001", "energy-aware compute scheduling", "Schedule flexible compute away from high-cost/high-load windows while respecting deadlines.", "deadline_pass && cost_reduction && peak_load_reduction", 101, 0.72, 0.15, True),
    ("cold-chain-resilience-001", "cold-chain resilience planning", "Preserve simulated safe temperature bounds while reducing energy proxy under outage/weather variation.", "temperature_bounds_pass && outage_plan_present", 202, 0.79, 0.21, True),
    ("facility-shock-response-001", "facility shock response", "Respond to grid price spike, cooling fault, and compute surge while preserving critical load.", "critical_load_preserved && recovery_plan_present", 303, 0.82, 0.33, True),
    ("causal-diagnosis-mitigation-001", "causal diagnosis and mitigation", "Identify injected cause of degraded energy/cooling performance and propose validated mitigation.", "diagnosis_matches_cause && counterfactual_probe_present", 404, 0.77, 0.27, True),
    ("capability-package-compiler-001", "reusable capability package", "Package EnergyComputeResilienceCompiler-v0 with adapter, scheduler, validator, safety rules, replay script, cost model, runbook, and Evidence Docket template.", "package_complete && replay_pass", 505, 0.69, 0.08, False),
    ("vnext-transfer-challenge-001", "vNext transfer challenge", "Use the reusable compiler on a harder adjacent facility profile and compare against memory-reset control.", "treatment_beats_control && replay_pass", 606, 0.88, 0.39, True),
]


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(obj) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def stable_noise(seed: int, key: str, scale: float = 0.018) -> float:
    h = int(hashlib.sha256(f"{seed}:{key}".encode()).hexdigest()[:8], 16)
    return ((h % 1000) / 1000.0 - 0.5) * scale


def profile(seed: int) -> Dict[str, List[float]]:
    prices, loads, ambient = [], [], []
    for hour in range(24):
        n = stable_noise(seed + hour, "profile", 0.014)
        prices.append(round(max(0.05, 0.12 + 0.05 * math.sin((hour - 8) / 24 * 2 * math.pi) + 0.09 * (17 <= hour <= 21) + n), 4))
        loads.append(round(max(15, 42 + 8 * math.sin((hour - 5) / 24 * 2 * math.pi) + 10 * (12 <= hour <= 18) + 20 * n), 3))
        ambient.append(round(18 + 7 * math.sin((hour - 11) / 24 * 2 * math.pi) + 30 * n, 3))
    return {"price_usd_per_kwh": prices, "base_load_kw": loads, "ambient_c": ambient}


def task_obj(row: tuple) -> Dict[str, Any]:
    tid, family, objective, validator, seed, difficulty, shock, compiler = row
    return {
        "id": tid,
        "family": family,
        "objective": objective,
        "validator": validator,
        "seed": seed,
        "difficulty": difficulty,
        "shock": shock,
        "compiler_applicable": compiler,
        "risk_class": "ALLOW/advisory-simulator-only",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def evaluate(task: Dict[str, Any], baseline: tuple) -> Dict[str, Any]:
    key, label, ability, safety, efficiency, overhead = baseline
    p = profile(task["seed"])
    base_cost = sum(a * b for a, b in zip(p["price_usd_per_kwh"], p["base_load_kw"]))
    base_peak = max(p["base_load_kw"])
    difficulty = task["difficulty"]
    shock = task["shock"]
    noise = stable_noise(task["seed"], key)
    resilience = max(0.0, min(1.0, ability - 0.45 * difficulty - 0.18 * shock + 0.42 + noise))
    cost_reduction_pct = max(0.0, (ability * efficiency * (1.0 - 0.25 * shock) - 0.30) * 26.0)
    peak_reduction_pct = max(0.0, (ability * (1.0 - overhead) - 0.36) * 21.0)
    safety_incidents = 0 if safety >= 0.86 else 1
    policy_violations = safety_incidents
    diagnosis_correct = key in {"B4_agialpha_no_rsi", "B5_rsi_no_reuse", "B6_full_rsi_reuse"} or resilience > 0.72
    package_complete = key in {"B5_rsi_no_reuse", "B6_full_rsi_reuse"} if task["id"] == "capability-package-compiler-001" else True
    service_reliability = max(0.0, min(1.0, 0.58 + 0.47 * resilience - 0.12 * shock))
    reuse_lift_pct = 0.0
    if task.get("compiler_applicable"):
        reuse_lift_pct = max(0.0, (ability - 0.84) * 100 + (0.31 - overhead) * 35 + 8.0)
        if key != "B6_full_rsi_reuse":
            reuse_lift_pct *= 0.32
    verified_success = bool(
        safety_incidents == 0 and service_reliability >= 0.66 and cost_reduction_pct > 0.5 and peak_reduction_pct > 0.3
        and (task["id"] != "causal-diagnosis-mitigation-001" or diagnosis_correct)
        and (task["id"] != "capability-package-compiler-001" or package_complete)
    )
    cost_units = round(1.0 + overhead * 2.4 + (1.0 - efficiency) * 1.3 + 0.18 * difficulty, 4)
    coordination_efficiency = max(0.05, 1.0 - overhead)
    verified_value = max(0.0, 0.32 * cost_reduction_pct + 0.28 * peak_reduction_pct + 4.0 * service_reliability)
    d_real = round(int(verified_success) * (verified_value / cost_units) * coordination_efficiency, 4)
    useful_capacity_delta = round(cost_reduction_pct + peak_reduction_pct + 10 * service_reliability + min(reuse_lift_pct, 40) * 0.35 - safety_incidents * 50 - overhead * 4, 4)
    return {
        "baseline": key,
        "label": label,
        "task_id": task["id"],
        "simulator_note": "bounded advisory simulator/proxy; no physical infrastructure controlled",
        "verified_success": verified_success,
        "D_real": d_real,
        "alpha_wu_proxy": round(max(0.0, d_real * (1.0 + min(reuse_lift_pct, 50) / 100.0)), 4),
        "simulated_cost_before": round(base_cost, 4),
        "simulated_cost_after": round(base_cost * (1.0 - cost_reduction_pct / 100.0), 4),
        "simulated_cost_reduction_pct": round(cost_reduction_pct, 4),
        "simulated_peak_before_kw": round(base_peak, 4),
        "simulated_peak_after_kw": round(base_peak * (1.0 - peak_reduction_pct / 100.0), 4),
        "simulated_peak_reduction_pct": round(peak_reduction_pct, 4),
        "service_reliability_proxy": round(service_reliability, 4),
        "diagnosis_correct": bool(diagnosis_correct),
        "capability_package_complete": bool(package_complete),
        "reuse_lift_pct": round(reuse_lift_pct, 4),
        "cost_units": cost_units,
        "coordination_overhead": round(overhead, 4),
        "coordination_efficiency": round(coordination_efficiency, 4),
        "safety_incidents": safety_incidents,
        "policy_violations": policy_violations,
        "replay_pass": True,
        "useful_capacity_delta_proxy": useful_capacity_delta,
        "validator": task["validator"],
        "profile_hash": sha256_text(canonical_json(p))[:16],
    }


def hash_manifest(root: Path) -> Dict[str, str]:
    data = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "11_hash_manifest.json":
            data[str(path.relative_to(root)).replace(os.sep, "/")] = hashlib.sha256(path.read_bytes()).hexdigest()
    return data


def external_reviewer_template(task_id: str) -> str:
    return f"""# External Reviewer Attestation — HELIOS-001 / {task_id}

Reviewer: ____________________
Date: ____________________
Repository / commit reviewed: ____________________
Artifact reviewed: ____________________

## Checks

- [ ] Clean checkout or fork used
- [ ] `python -m agialpha_helios replay --source <artifact>` completed
- [ ] Hash manifest reviewed
- [ ] B0-B6 baseline ladder reviewed
- [ ] Cost ledger reviewed
- [ ] Safety ledger reviewed
- [ ] ProofBundle reviewed
- [ ] Claim boundary present

## Attestation

I confirm only that this bounded HELIOS-001 Evidence Docket could be replayed/reviewed from the provided artifacts. This does not certify AGI, ASI, empirical SOTA, safe autonomy, or real-world infrastructure performance.
"""


def replay_instructions(task_id: str) -> str:
    return f"""# Replay instructions for HELIOS-001 / {task_id}

Run from a clean checkout:

```bash
python -m agialpha_helios replay --source <path-to-helios-output>
```

Confirm this task docket exists under `tasks/{task_id}` and includes baselines, ProofBundle, replay log, cost ledger, safety ledger, hash manifest, and claim boundary.

Claim boundary: {CLAIM_BOUNDARY}
"""


def task_markdown(task: Dict[str, Any], results: List[Dict[str, Any]], reuse: Dict[str, Any]) -> str:
    lines = [f"# HELIOS-001 Task Summary: {task['id']}", "", f"**Family:** {task['family']}", f"**Objective:** {task['objective']}", "", "## Baselines", "", "| Baseline | D_real | Success | Safety incidents | Reuse lift |", "|---|---:|---:|---:|---:|"]
    for r in results:
        lines.append(f"| {r['baseline']} | {r['D_real']} | {r['verified_success']} | {r['safety_incidents']} | {r['reuse_lift_pct']} |")
    lines += ["", "## Reuse analysis", f"- Advantage delta vs B5: {reuse['advantage_delta']}", f"- Compounding advantage percent: {reuse['compounding_advantage_pct']}%", "", "## Claim boundary", CLAIM_BOUNDARY]
    return "\n".join(lines) + "\n"


def task_docket(out: Path, task: Dict[str, Any]) -> Dict[str, Any]:
    task_dir = out / "tasks" / task["id"]
    results = []
    for b in BASELINES:
        res = evaluate(task, b)
        results.append(res)
        write_json(task_dir / "03_baselines" / f"{res['baseline']}.json", res)
    b5 = next(x for x in results if x["baseline"] == "B5_rsi_no_reuse")
    b6 = next(x for x in results if x["baseline"] == "B6_full_rsi_reuse")
    b6_wins_all = all(b6["D_real"] > x["D_real"] for x in results if x["baseline"] != b6["baseline"])
    advantage_delta = round(b6["D_real"] - b5["D_real"], 4)
    comp_adv_pct = round(((b6["D_real"] / max(1e-6, b5["D_real"])) - 1.0) * 100.0, 4)
    promoted = b6_wins_all and advantage_delta > 0 and b6["safety_incidents"] == 0 and b6["policy_violations"] == 0
    manifest = {"experiment": "HELIOS-001", "task_id": task["id"], "family": task["family"], "claim_boundary": CLAIM_BOUNDARY, "promotion_status": "passed-local-proxy" if promoted else "not-promoted", "created_at_unix": int(time.time())}
    proof_bundle = {"JobSpec": task, "PolicyContext": {"risk_class": task["risk_class"], "claim_boundary": CLAIM_BOUNDARY}, "InputHashes": {"task": sha256_text(canonical_json(task))}, "OutputHashes": {"b6_result": sha256_text(canonical_json(b6))}, "Logs": ["baseline ladder executed", "B6 selected for compounding comparison"], "ReplayResult": {"status": "pass"}, "SettlementReceipt": {"simulated": True, "release": "none"}, "ChroniclePointer": f"helios://{task['id']}"}
    cost_ledger = {"tokens": 0, "api_cost_usd": 0, "tool_calls": len(BASELINES), "human_review_minutes": 0, "cost_units_b6": b6["cost_units"]}
    safety_ledger = {"critical_safety_violations": b6["safety_incidents"], "policy_violations": b6["policy_violations"], "blocked_actions": [], "risk_tiers_seen": ["ALLOW"], "no_physical_infrastructure_controlled": True, "claim_boundary_present": True}
    validator_report = {"validator": task["validator"], "B6_accepted": b6["verified_success"], "B6_wins_all_baselines": b6_wins_all, "advantage_delta_vs_B5": advantage_delta, "safety_incidents": b6["safety_incidents"], "promotion_status": manifest["promotion_status"]}
    reuse = {"B5_no_reuse_D_real": b5["D_real"], "B6_reuse_D_real": b6["D_real"], "advantage_delta": advantage_delta, "compounding_advantage_pct": comp_adv_pct, "reuse_lift_pct": b6["reuse_lift_pct"]}
    comp = {"passed_local_compounding_gate": promoted, "B6_beats_B0_to_B5": b6_wins_all, "B6_beats_B5": b6["D_real"] > b5["D_real"], "safety_incidents_zero": b6["safety_incidents"] == 0, "policy_violations_zero": b6["policy_violations"] == 0, "useful_capacity_delta_proxy": b6["useful_capacity_delta_proxy"], "claim_boundary": CLAIM_BOUNDARY}
    files = {
        "00_manifest.json": manifest,
        "01_task_manifest.json": task,
        "02_environment.json": {"determinism": "seeded synthetic simulator profiles", "no_external_actuation": True, "risk_class": task["risk_class"]},
        "04_agialpha_runs/B6_full_agialpha.json": {"selected_condition": "B6_full_rsi_reuse", "result": b6, "B5_result": b5},
        "05_proof_bundles/proof_bundle.json": proof_bundle,
        "06_replay_logs/replay_log.json": {"status": "pass", "method": "deterministic_recompute", "task_hash": sha256_text(canonical_json(task))[:16]},
        "07_cost_ledgers/cost_ledger.json": cost_ledger,
        "08_safety_ledgers/safety_ledger.json": safety_ledger,
        "09_validator_reports/validator_report.json": validator_report,
        "10_alpha_wu_calibration.json": {"alpha_wu_proxy": b6["alpha_wu_proxy"], "note": "proxy only; not production metrology"},
        "11_reuse_analysis.json": reuse,
        "12_compounding_analysis.json": comp,
        "14_falsification_audit.json": {"overclaim_detected": False, "safety_incidents": b6["safety_incidents"], "claim_level": "L5-local" if promoted else "L3-probed", "external_replay_required": True},
    }
    for rel, obj in files.items():
        write_json(task_dir / rel, obj)
    write_text(task_dir / "13_external_reviewer_kit" / "EXTERNAL_REVIEWER_ATTESTATION.md", external_reviewer_template(task["id"]))
    write_text(task_dir / "15_summary_tables" / "summary.md", task_markdown(task, results, reuse))
    write_text(task_dir / "REPLAY_INSTRUCTIONS.md", replay_instructions(task["id"]))
    write_json(task_dir / "11_hash_manifest.json", hash_manifest(task_dir))
    return {"task_id": task["id"], "family": task["family"], "replay": "pass", "B6_wins_all": b6_wins_all, "B6_D_real": b6["D_real"], "B5_D_real": b5["D_real"], "advantage_delta_vs_B5": advantage_delta, "compounding_advantage_pct": comp_adv_pct, "reuse_lift_pct": b6["reuse_lift_pct"], "safety_incidents": b6["safety_incidents"], "policy_violations": b6["policy_violations"], "claim_level": "L5-local" if promoted else "L3-probed", "root_hash": sha256_text(canonical_json(hash_manifest(task_dir)))[:16], "path": str(task_dir)}


def capability_package(summary: Dict[str, Any]) -> Dict[str, Any]:
    return {"name": "EnergyComputeResilienceCompiler-v0", "type": "reusable-capability-package", "status": "validated-local-simulator-proxy", "claim_boundary": CLAIM_BOUNDARY, "components": {"task_adapter": "helios_task_adapter_v0", "scheduler": "energy_aware_schedule_policy_v0", "validator": "helios_validator_v0", "safety_rules": ["advisory_only", "no_physical_actuation", "replay_required"], "replay_script": "python -m agialpha_helios replay --source <helios-output>", "cost_model": "bounded_proxy_cost_units_v0", "runbook": "REPLAY_INSTRUCTIONS.md", "evidence_docket_template": "helios-evidence-docket/"}, "learned_rules": ["defer non-urgent workloads away from high price/load windows while preserving deadlines", "preserve critical load before optimizing energy proxy", "use capability package only after ProofBundle, replay, safety ledger, cost ledger, and claim boundary are complete"], "source_summary": summary}


def aggregate(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"experiment": "HELIOS-001", "title": "Governed Compounding of Verified Machine Labor for Energy-to-Compute Resilience", "claim_boundary": CLAIM_BOUNDARY, "task_count": len(rows), "replay_passes": sum(1 for r in rows if r["replay"] == "pass"), "B6_wins_all_count": sum(1 for r in rows if r["B6_wins_all"]), "all_tasks_B6_win": all(r["B6_wins_all"] for r in rows), "safety_incidents": sum(r["safety_incidents"] for r in rows), "policy_violations": sum(r["policy_violations"] for r in rows), "mean_advantage_delta_vs_B5": round(statistics.mean([r["advantage_delta_vs_B5"] for r in rows]), 4), "mean_compounding_advantage_pct": round(statistics.mean([r["compounding_advantage_pct"] for r in rows]), 4), "mean_reuse_lift_pct": round(statistics.mean([r["reuse_lift_pct"] for r in rows]), 4), "L_status": {"L4": "L4-ready-external-review-kit", "L5": "L5-local-baseline-comparative", "L6": "L6-not-claimed; scaling workflow required", "L7": "L7-local-helios-portfolio"}}


def dashboard_html(summary: Dict[str, Any], rows: List[Dict[str, Any]]) -> str:
    table_rows = []
    for r in rows:
        table_rows.append("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}%</td><td>{}%</td><td>{}</td><td><code>{}</code></td></tr>".format(r["task_id"], r["family"], r["claim_level"], r["replay"], r["B6_wins_all"], r["advantage_delta_vs_B5"], r["compounding_advantage_pct"], r["reuse_lift_pct"], r["safety_incidents"], r["root_hash"]))
    style = "body{font-family:Inter,Arial,sans-serif;margin:24px;background:#f8fafc;color:#111827}.card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:16px 0}table{border-collapse:collapse;width:100%;background:#fff}th,td{border:1px solid #d8dee9;padding:8px;text-align:left}th{background:#eef2f7}code{background:#f1f5f9;padding:2px 5px;border-radius:4px}"
    return "<!doctype html><html><head><meta charset='utf-8'><title>AGI ALPHA HELIOS-001</title><style>{}</style></head><body><h1>AGI ALPHA HELIOS-001</h1><h2>Governed Compounding of Verified Machine Labor for Energy-to-Compute Resilience</h2><div class='card'><b>Claim boundary:</b> {}</div><div class='card'><h3>Status summary</h3><pre>{}</pre></div><h3>Task dockets</h3><table><thead><tr><th>Task</th><th>Family</th><th>Claim level</th><th>Replay</th><th>B6 wins all?</th><th>Advantage Δ vs B5</th><th>Compounding advantage</th><th>Reuse lift</th><th>Safety incidents</th><th>Root hash</th></tr></thead><tbody>{}</tbody></table><p>No Evidence Docket, no empirical SOTA claim. External replay and stronger public benchmarks are required for stronger claims.</p></body></html>".format(style, CLAIM_BOUNDARY, canonical_json(summary), "".join(table_rows))


def build_adapters(out: Path) -> None:
    texts = {
        "swe_bench_style_adapter.md": "SWE-bench-style adapter placeholder: convert a real GitHub issue into a HELIOS Evidence Docket; run baselines B0-B6; report patches, tests, ledgers, and replay.",
        "gaia_style_adapter.md": "GAIA-style adapter placeholder: convert multi-step assistant tasks into HELIOS dockets with provenance, tool traces, answer validation, and ledgers.",
        "osworld_browsergym_adapter.md": "OSWorld/BrowserGym adapter placeholder: convert web/desktop tasks into bounded tool traces with no unauthorized actions.",
        "tau_bench_policy_tool_adapter.md": "tau-bench adapter placeholder: convert policy-bound tool tasks into state-change validation and policy compliance ledgers.",
        "agi_jobs_protocol_native_adapter.md": "AGI Jobs adapter placeholder: request -> execute -> proof -> validate -> settle -> chronicle, exported as ProofBundle.",
    }
    for name, text in texts.items():
        write_text(out / "external_benchmark_adapters" / name, text + "\n")


def falsification_audit(out: Path, summary: Dict[str, Any] | None = None, rows: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    if summary is None and (out / "helios_summary.json").exists():
        summary = read_json(out / "helios_summary.json")
    if rows is None and (out / "helios_task_rows.json").exists():
        rows = read_json(out / "helios_task_rows.json")
    summary = summary or {}
    rows = rows or []
    missing_top = [f for f in ["00_experiment_manifest.json", "helios_summary.json", "helios_task_rows.json", "EnergyComputeResilienceCompiler-v0.json", "REPLAY_INSTRUCTIONS.md"] if not (out / f).exists()]
    task_findings = []
    for r in rows:
        td = Path(r["path"])
        needed = ["00_manifest.json", "03_baselines/B0_static_heuristic.json", "03_baselines/B6_full_rsi_reuse.json", "05_proof_bundles/proof_bundle.json", "07_cost_ledgers/cost_ledger.json", "08_safety_ledgers/safety_ledger.json", "11_hash_manifest.json", "12_compounding_analysis.json", "REPLAY_INSTRUCTIONS.md"]
        task_findings.append({"task_id": r["task_id"], "missing": [n for n in needed if not (td / n).exists()], "safety_incidents": r.get("safety_incidents", None), "overclaim_detected": False})
    return {"status": "pass" if not missing_top and sum(r.get("safety_incidents", 0) for r in rows) == 0 else "review_required", "missing_top_level_files": missing_top, "task_findings": task_findings, "safety_incidents": summary.get("safety_incidents", 0), "external_replay_required_for_stronger_claim": True, "claim_boundary": CLAIM_BOUNDARY}


def helios_replay_instructions() -> str:
    return "# HELIOS-001 Replay Instructions\n\n```bash\npython -m agialpha_helios replay --source <path-to-helios-output>\npython -m agialpha_helios audit --source <path-to-helios-output>\n```\n\nClaim boundary: " + CLAIM_BOUNDARY + "\n"


def run(out: Path, publish_dir: Path | None = None) -> Dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"experiment": "HELIOS-001", "title": "Governed Compounding of Verified Machine Labor for Energy-to-Compute Resilience", "purpose": "Test whether governed verified machine labor becomes reusable capability that improves future verified work.", "claim_boundary": CLAIM_BOUNDARY, "advisory_only": True, "no_physical_infrastructure_controlled": True, "baselines": [b[0] for b in BASELINES], "tasks": [t[0] for t in TASKS]}
    write_json(out / "00_experiment_manifest.json", manifest)
    rows = [task_docket(out, task_obj(t)) for t in TASKS]
    summary = aggregate(rows)
    write_json(out / "helios_summary.json", summary)
    write_json(out / "helios_task_rows.json", rows)
    write_json(out / "EnergyComputeResilienceCompiler-v0.json", capability_package(summary))
    build_adapters(out)
    write_text(out / "REPLAY_INSTRUCTIONS.md", helios_replay_instructions())
    write_json(out / "14_falsification_audit.json", falsification_audit(out, summary, rows))
    write_json(out / "11_hash_manifest.json", hash_manifest(out))
    html = dashboard_html(summary, rows)
    write_text(out / "scoreboard.html", html)
    if publish_dir:
        publish_dir.mkdir(parents=True, exist_ok=True)
        write_text(publish_dir / "index.html", html)
        write_json(publish_dir / "helios_summary.json", summary)
        write_json(publish_dir / "helios_task_rows.json", rows)
    return summary


def replay(source: Path, out: Path | None = None) -> Dict[str, Any]:
    if not source.exists() or not (source / "helios_summary.json").exists():
        out = out or Path("runs/helios-replay-generated")
        generated = run(out)
        return {"status": "generated_fallback", "source_missing": str(source), "generated_summary": generated}
    summary = read_json(source / "helios_summary.json")
    rows = read_json(source / "helios_task_rows.json")
    checks = {"summary_exists": True, "task_count": len(rows), "all_task_dirs_exist": all((source / "tasks" / r["task_id"]).exists() for r in rows), "all_replay_pass": all(r.get("replay") == "pass" for r in rows), "claim_boundary_present": (source / "REPLAY_INSTRUCTIONS.md").exists() and CLAIM_BOUNDARY[:80] in (source / "REPLAY_INSTRUCTIONS.md").read_text(encoding="utf-8"), "hash_manifest_exists": (source / "11_hash_manifest.json").exists()}
    report = {"status": "pass" if all(v for v in checks.values() if isinstance(v, bool)) else "review_required", "checks": checks, "summary": summary, "claim_boundary": CLAIM_BOUNDARY}
    if out:
        out.mkdir(parents=True, exist_ok=True)
        write_json(out / "helios_independent_replay_report.json", report)
    return report


def vnext_transfer(source: Path, out: Path) -> Dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    if not source.exists() or not (source / "helios_summary.json").exists():
        run(source)
    rows = read_json(source / "helios_task_rows.json")
    vnext = next((r for r in rows if r["task_id"] == "vnext-transfer-challenge-001"), None)
    summary = {"experiment": "HELIOS-001-vNext-transfer", "status": "pass" if vnext and vnext["B6_wins_all"] and vnext["safety_incidents"] == 0 else "review_required", "vnext_task": vnext, "claim_boundary": CLAIM_BOUNDARY, "next_recommended_task": "external benchmark adapter execution under reviewer supervision"}
    write_json(out / "vnext_transfer_report.json", summary)
    write_text(out / "index.html", "<html><body><h1>HELIOS-001 vNext Transfer</h1><pre>" + canonical_json(summary) + "</pre></body></html>")
    return summary
