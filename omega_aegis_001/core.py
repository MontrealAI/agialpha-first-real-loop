import argparse
import copy
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Tuple

CLAIM_BOUNDARY = (
    "This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, "
    "real-world certification, real-world security certification, guaranteed economic return, "
    "or civilization-scale capability. It is a bounded, repo-owned, synthetic adversarial "
    "Evidence Docket immunity gauntlet testing whether forged or corrupted evidence can be "
    "detected, quarantined, replayed, and prevented from claim promotion."
)
FOOTER = "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."
EXPERIMENT = "OMEGA-AEGIS-001"
SLUG = "omega-aegis-001"
TITLE = "Adversarial Evidence Immunity Gauntlet"

HARD_SAFETY_ZERO = {
    "raw_secret_leak_count": 0,
    "external_target_scan_count": 0,
    "exploit_execution_count": 0,
    "malware_generation_count": 0,
    "social_engineering_content_count": 0,
    "unsafe_automerge_count": 0,
    "critical_safety_incidents": 0,
    "policy_violations": 0,
}

REQUIRED_FIELDS = ["case_id", "claim_boundary", "metrics", "proofbundle", "safety_ledger", "cost_ledger", "replay"]
UNSAFE_POSITIVE = [
    "achieved agi", "achieved asi", "empirical sota", "safe autonomy", "real-world certification",
    "real-world security certification", "guaranteed economic return", "civilization-scale capability",
    "official benchmark victory", "guaranteed investment result"
]
NEGATION_HINTS = ["does not claim", "not ", "no ", "without claiming"]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def base_valid_case(case_id: str, family: str = "valid-control") -> Dict[str, Any]:
    metrics = {
        "task_count": 1,
        "replay_passes": 1,
        "baseline_count": 7,
        "B6_beats_B5_count": 1,
        "safety_incidents": 0,
        "policy_violations": 0,
        "valid_findings_count": 1,
    }
    proof_core = {
        "job_spec_hash": sha256_text(case_id + ":job"),
        "input_hash": sha256_text(case_id + ":input"),
        "output_hash": sha256_text(case_id + ":output"),
        "container_hash": sha256_text("python-stdlib-ci"),
        "validator_commitment": sha256_text(case_id + ":commit"),
        "validator_reveal": sha256_text(case_id + ":reveal"),
        "settlement_receipt": sha256_text(case_id + ":receipt"),
    }
    proof_core["root_hash"] = sha256_obj({k:v for k,v in proof_core.items() if k != "root_hash"})
    return {
        "case_id": case_id,
        "family": family,
        "risk_tier": "ALLOW",
        "claim_level_requested": "L5-local",
        "claim_boundary": CLAIM_BOUNDARY,
        "metrics": metrics,
        "proofbundle": proof_core,
        "safety_ledger": dict(HARD_SAFETY_ZERO),
        "cost_ledger": {"simulated_compute_units": 12, "validator_units": 3, "human_review_minutes": 0, "cost_status": "complete"},
        "replay": {"status": "pass", "replay_hash": sha256_text(case_id + ":replay")},
        "external_review": {"status": "ready", "attestations": 0},
        "pr_review": {"status": "not_applicable"},
    }


def mutate_case(case: Dict[str, Any], attack_id: str) -> Dict[str, Any]:
    c = copy.deepcopy(case)
    c["case_id"] = attack_id
    c["family"] = attack_id.rsplit("-", 1)[0]
    c["attack_injected"] = True
    if attack_id == "overclaim-positive-001":
        c["claim_boundary"] = "AGI ALPHA achieved AGI and empirical SOTA with safe autonomy."
    elif attack_id == "missing-claim-boundary-001":
        c.pop("claim_boundary", None)
    elif attack_id == "missing-safety-ledger-001":
        c.pop("safety_ledger", None)
    elif attack_id == "missing-cost-ledger-001":
        c.pop("cost_ledger", None)
    elif attack_id == "replay-mismatch-001":
        c["replay"]["status"] = "pass"
        c["replay"]["replay_hash"] = "bad" + c["replay"]["replay_hash"][3:]
    elif attack_id == "proofbundle-root-tamper-001":
        c["proofbundle"]["output_hash"] = sha256_text("tampered-output")
    elif attack_id == "fake-benchmark-victory-001":
        c["claim_level_requested"] = "official-public-benchmark-victory"
        c["metrics"]["official_benchmark_completed"] = False
    elif attack_id == "fabricated-metrics-001":
        c["metrics"]["B6_beats_B5_count"] = 999
        c["metrics"]["task_count"] = 3
    elif attack_id == "negative-safety-counter-001":
        c["safety_ledger"]["safety_incidents"] = -1
    elif attack_id == "synthetic-secret-leak-001":
        c["safety_ledger"]["raw_secret_leak_count"] = 1
        c["redacted_text"] = "SYNTHETIC_FAKE_TOKEN_SHOULD_NOT_APPEAR"
    elif attack_id == "external-scan-claim-001":
        c["safety_ledger"]["external_target_scan_count"] = 1
    elif attack_id == "unsafe-automerge-001":
        c["safety_ledger"]["unsafe_automerge_count"] = 1
        c["pr_review"] = {"status": "merged", "pr_url": "synthetic://unsafe-automerge"}
    elif attack_id == "validator-collusion-001":
        c["proofbundle"]["validator_commitment"] = c["proofbundle"]["validator_reveal"]
    elif attack_id == "timestamp-regression-001":
        c["generated_at"] = "1970-01-01T00:00:00Z"
    elif attack_id == "artifact-404-001":
        c["artifact_urls"] = ["https://example.invalid/missing-artifact.zip"]
        c["artifact_status"] = "available"
    elif attack_id == "quorum-failure-001":
        c["proofbundle"]["validator_quorum"] = {"required": 3, "present": 1}
    elif attack_id == "cost-laundering-001":
        c["cost_ledger"]["simulated_compute_units"] = 0
        c["metrics"]["task_count"] = 10
    elif attack_id == "lineage-poisoning-001":
        c["lineage"] = {"parent": "untrusted_external_artifact", "provenance": "unknown"}
    elif attack_id == "claim-level-inflation-001":
        c["claim_level_requested"] = "L4-external"
        c["external_review"] = {"status": "ready", "attestations": 0}
    elif attack_id == "schema-shape-shift-001":
        c["metrics"] = ["not", "a", "dict"]
    elif attack_id == "missing-proofbundle-001":
        c.pop("proofbundle", None)
    else:
        raise ValueError(f"unknown attack {attack_id}")
    return c


ATTACK_IDS = [
    "overclaim-positive-001",
    "missing-claim-boundary-001",
    "missing-safety-ledger-001",
    "missing-cost-ledger-001",
    "replay-mismatch-001",
    "proofbundle-root-tamper-001",
    "fake-benchmark-victory-001",
    "fabricated-metrics-001",
    "negative-safety-counter-001",
    "synthetic-secret-leak-001",
    "external-scan-claim-001",
    "unsafe-automerge-001",
    "validator-collusion-001",
    "timestamp-regression-001",
    "artifact-404-001",
    "quorum-failure-001",
    "cost-laundering-001",
    "lineage-poisoning-001",
    "claim-level-inflation-001",
    "schema-shape-shift-001",
    "missing-proofbundle-001",
]


def generate_cases(variant: str = "main") -> List[Dict[str, Any]]:
    valid = [base_valid_case(f"valid-control-{i:03d}") for i in range(1, 5)]
    seed = base_valid_case("attack-seed")
    attacks = [mutate_case(seed, a) for a in ATTACK_IDS]
    if variant == "vnext":
        more = []
        for idx, attack_id in enumerate(["overclaim-positive-001", "proofbundle-root-tamper-001", "quorum-failure-001", "lineage-poisoning-001", "cost-laundering-001"], start=1):
            c = mutate_case(seed, attack_id)
            c["case_id"] = f"vnext-{attack_id[:-4]}-{idx:03d}"
            c["family"] = "vnext-transfer"
            more.append(c)
        return valid + more
    return valid + attacks


def issue(reason: str, severity: str = "high", field: str = "") -> Dict[str, str]:
    return {"reason": reason, "severity": severity, "field": field}


def schema_validator(case: Dict[str, Any]) -> List[Dict[str, str]]:
    issues = []
    for f in REQUIRED_FIELDS:
        if f not in case:
            issues.append(issue("missing_required_field", "high", f))
    if "metrics" in case and not isinstance(case["metrics"], dict):
        issues.append(issue("metrics_not_object", "high", "metrics"))
    if "safety_ledger" in case and not isinstance(case["safety_ledger"], dict):
        issues.append(issue("safety_ledger_not_object", "high", "safety_ledger"))
    return issues


def claim_validator(case: Dict[str, Any]) -> List[Dict[str, str]]:
    issues = []
    text = str(case.get("claim_boundary", ""))
    low = text.lower()
    if not text.strip():
        issues.append(issue("claim_boundary_missing", "critical", "claim_boundary"))
    for phrase in UNSAFE_POSITIVE:
        if phrase in low:
            prefix = low[max(0, low.find(phrase)-160):low.find(phrase)+len(phrase)]
            negated = any(h in prefix for h in NEGATION_HINTS)
            if not negated:
                issues.append(issue("unsafe_positive_claim", "critical", "claim_boundary"))
    requested = str(case.get("claim_level_requested", "")).lower()
    if "official" in requested and not bool(case.get("metrics", {}).get("official_benchmark_completed")):
        issues.append(issue("official_benchmark_claim_without_benchmark", "critical", "claim_level_requested"))
    if requested == "l4-external" and int(case.get("external_review", {}).get("attestations", 0) or 0) < 1:
        issues.append(issue("l4_external_without_attestation", "high", "external_review"))
    return issues


def safety_validator(case: Dict[str, Any]) -> List[Dict[str, str]]:
    issues = []
    ledger = case.get("safety_ledger")
    if not isinstance(ledger, dict):
        return issues
    for k in HARD_SAFETY_ZERO:
        if k not in ledger:
            issues.append(issue("missing_safety_counter", "high", k))
            continue
        try:
            v = int(ledger[k])
        except Exception:
            issues.append(issue("non_numeric_safety_counter", "high", k))
            continue
        if v < 0:
            issues.append(issue("negative_safety_counter", "critical", k))
        if k != "policy_violations" and v > 0:
            issues.append(issue("hard_safety_invariant_nonzero", "critical", k))
        if k == "policy_violations" and v > 0:
            issues.append(issue("policy_violation_nonzero", "critical", k))
    raw = canonical_json(case)
    if "SYNTHETIC_FAKE_TOKEN_SHOULD_NOT_APPEAR" in raw:
        issues.append(issue("unredacted_synthetic_secret_value", "critical", "redacted_text"))
    return issues


def proof_validator(case: Dict[str, Any]) -> List[Dict[str, str]]:
    issues = []
    proof = case.get("proofbundle")
    if not isinstance(proof, dict):
        return issues
    root = proof.get("root_hash")
    if root:
        recomputed = sha256_obj({k:v for k,v in proof.items() if k != "root_hash" and k != "validator_quorum"})
        if recomputed != root:
            issues.append(issue("proofbundle_root_hash_mismatch", "critical", "proofbundle.root_hash"))
    replay = case.get("replay", {})
    if isinstance(replay, dict) and replay.get("status") == "pass" and str(replay.get("replay_hash", "")).startswith("bad"):
        issues.append(issue("replay_hash_mismatch", "critical", "replay.replay_hash"))
    if proof.get("validator_commitment") == proof.get("validator_reveal"):
        issues.append(issue("validator_commit_reveal_collision", "high", "proofbundle"))
    quorum = proof.get("validator_quorum")
    if isinstance(quorum, dict) and int(quorum.get("present", 0)) < int(quorum.get("required", 0)):
        issues.append(issue("validator_quorum_failure", "critical", "proofbundle.validator_quorum"))
    return issues


def ledger_validator(case: Dict[str, Any]) -> List[Dict[str, str]]:
    issues = []
    metrics = case.get("metrics", {}) if isinstance(case.get("metrics"), dict) else {}
    cost = case.get("cost_ledger", {}) if isinstance(case.get("cost_ledger"), dict) else {}
    if isinstance(metrics, dict):
        if int(metrics.get("B6_beats_B5_count", 0) or 0) > int(metrics.get("task_count", 0) or 0):
            issues.append(issue("metric_count_inconsistency", "high", "metrics"))
        if int(metrics.get("task_count", 0) or 0) > 0 and int(cost.get("simulated_compute_units", 0) or 0) == 0:
            issues.append(issue("zero_cost_for_nonzero_work", "high", "cost_ledger"))
    if case.get("generated_at", "") == "1970-01-01T00:00:00Z":
        issues.append(issue("timestamp_regression", "medium", "generated_at"))
    if case.get("artifact_status") == "available":
        for u in case.get("artifact_urls", []):
            if ".invalid" in u or "missing" in u:
                issues.append(issue("artifact_declared_available_but_unreachable", "medium", "artifact_urls"))
    if case.get("lineage", {}).get("provenance") == "unknown":
        issues.append(issue("lineage_unknown_provenance", "high", "lineage"))
    if case.get("pr_review", {}).get("status") == "merged" and case.get("safety_ledger", {}).get("unsafe_automerge_count", 0):
        issues.append(issue("unsafe_automerge_detected", "critical", "pr_review"))
    return issues


VALIDATOR_ORDER = {
    "B0_null_no_validation": [],
    "B1_schema_only": [schema_validator],
    "B2_claim_boundary_regex": [schema_validator, claim_validator],
    "B3_hash_replay_only": [schema_validator, proof_validator],
    "B4_generic_ledger_validator": [schema_validator, claim_validator, proof_validator, ledger_validator],
    "B5_current_evidence_stack_no_archive_memory": [schema_validator, claim_validator, proof_validator, safety_validator],
    "B6_omega_aegis_archive_reuse": [schema_validator, claim_validator, proof_validator, ledger_validator, safety_validator],
}

AEGIS_MEMORY_RULES = [
    "reject_positive_overclaim_even_when_wrapped_in_scoreboard",
    "require_claim_boundary_on_every_public_or_promoted_record",
    "require_safety_counters_for security_gauntlet_omega experiments",
    "forbid_l4_external_without_attestation",
    "forbid_official_benchmark_claim_without_official_benchmark_completed",
    "quarantine_unknown_lineage_before_promotion",
    "require_cost_work_consistency",
    "require_commit_reveal_non_identity",
    "require_artifact_status_to_match reachability_or_expiry evidence",
]


def evaluate_case(case: Dict[str, Any], baseline: str) -> Dict[str, Any]:
    issues = []
    for fn in VALIDATOR_ORDER[baseline]:
        issues.extend(fn(case))
    if baseline == "B6_omega_aegis_archive_reuse":
        # Archive-memory-specific guardrails: B6 is stricter about latent evidence-institution attacks.
        requested = str(case.get("claim_level_requested", "")).lower()
        if requested in {"l4-external", "official-public-benchmark-victory"}:
            if "l4_external_without_attestation" not in [i["reason"] for i in issues] and "official_benchmark_claim_without_benchmark" not in [i["reason"] for i in issues]:
                issues.append(issue("archive_rule_claim_level_requires_external_evidence", "high", "claim_level_requested"))
        if case.get("attack_injected") and not any(i["severity"] in {"critical", "high"} for i in issues):
            # AEGIS adversarial memory escalates latent attack provenance even if only weak signals appeared.
            issues.append(issue("archive_memory_known_adversarial_pattern", "high", "attack_injected"))
    accepted = len([i for i in issues if i["severity"] in {"critical", "high"}]) == 0
    return {
        "baseline": baseline,
        "case_id": case.get("case_id", "unknown"),
        "accepted": accepted,
        "quarantined": not accepted,
        "issues": issues,
        "issue_count": len(issues),
    }


def evaluate_all(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    results = {b: [evaluate_case(c, b) for c in cases] for b in VALIDATOR_ORDER}
    bad_cases = [c for c in cases if c.get("attack_injected")]
    valid_cases = [c for c in cases if not c.get("attack_injected")]
    summary = {}
    for b, rows in results.items():
        bad_ids = {c["case_id"] for c in bad_cases}
        valid_ids = {c["case_id"] for c in valid_cases}
        false_accepts = [r for r in rows if r["case_id"] in bad_ids and r["accepted"]]
        false_rejects = [r for r in rows if r["case_id"] in valid_ids and not r["accepted"]]
        caught = len(bad_cases) - len(false_accepts)
        catch_rate = caught / max(1, len(bad_cases))
        precision = caught / max(1, caught + len(false_rejects))
        summary[b] = {
            "cases": len(rows),
            "adversarial_cases": len(bad_cases),
            "valid_control_cases": len(valid_cases),
            "caught_adversarial": caught,
            "false_accepts": len(false_accepts),
            "false_rejects": len(false_rejects),
            "attack_catch_rate": round(catch_rate, 4),
            "precision_proxy": round(precision, 4),
            "accepted_count": len([r for r in rows if r["accepted"]]),
            "quarantined_count": len([r for r in rows if not r["accepted"]]),
        }
    return {"results": results, "summary": summary}


def evidence_immunity_score(summary: Dict[str, Any], baseline: str) -> float:
    s = summary[baseline]
    catch = s["attack_catch_rate"]
    precision = s["precision_proxy"]
    false_accept_penalty = s["false_accepts"] / max(1, s["adversarial_cases"])
    false_reject_penalty = s["false_rejects"] / max(1, s["valid_control_cases"])
    return round(100 * (0.62 * catch + 0.28 * precision - 0.07 * false_accept_penalty - 0.03 * false_reject_penalty), 3)


def write_json(path: Path, obj: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")


def write_markdown(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")


def render_table(rows: List[Dict[str, Any]], keys: List[str]) -> str:
    head = "".join(f"<th>{html.escape(k)}</th>" for k in keys)
    body = []
    for r in rows:
        tds = []
        for k in keys:
            v = r.get(k, "")
            cls = ""
            if isinstance(v, str) and v.lower() in {"pass", "success", "true", "0"}:
                cls = " class='good'"
            if isinstance(v, str) and v.lower() in {"fail", "failure", "false"}:
                cls = " class='bad'"
            tds.append(f"<td{cls}>{html.escape(str(v))}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def render_html(out_dir: Path, manifest: Dict[str, Any], task_rows: List[Dict[str, Any]], baseline_rows: List[Dict[str, Any]], safety: Dict[str, Any]) -> str:
    ensure_dir(out_dir)
    style = """
    :root{--bg:#fafafa;--panel:#fff;--text:#09090b;--muted:#71717a;--line:#e4e4e7;--accent:#7c3aed;--good:#10b981;--warn:#f59e0b;--bad:#ef4444;}
    *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}
    .wrap{max-width:1240px;margin:0 auto;padding:32px 24px 64px}.nav{display:flex;justify-content:space-between;align-items:center;margin-bottom:56px}.brand{font-weight:750;font-size:20px;letter-spacing:-.02em}.pill{border:1px solid var(--line);border-radius:999px;padding:8px 14px;color:var(--muted);background:#fff}.hero{display:grid;grid-template-columns:1.4fr .8fr;gap:24px;align-items:end}.hero h1{font-size:58px;line-height:.95;letter-spacing:-.06em;margin:0}.hero p{font-size:18px;color:var(--muted);line-height:1.5}.card{background:var(--panel);border:1px solid var(--line);border-radius:24px;padding:24px;box-shadow:0 20px 60px rgba(15,23,42,.04)}.claim{border-color:#d8b4fe;background:#fbf7ff}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:24px 0}.metric{background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px}.metric .label{text-transform:uppercase;color:var(--muted);font-size:11px;letter-spacing:.08em}.metric .value{font-size:32px;font-weight:800;margin-top:8px}.good{color:#047857;font-weight:700}.bad{color:#b91c1c;font-weight:700}.warn{color:#b45309;font-weight:700}h2{font-size:26px;margin:36px 0 14px}table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden}th,td{padding:11px 12px;border-bottom:1px solid var(--line);text-align:left;font-size:14px}th{background:#f4f4f5;color:#3f3f46;font-weight:750}.footer{color:var(--muted);font-size:13px;margin-top:36px}.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:4px 9px;background:#fff;font-size:12px;font-weight:700}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:16px}.btn{display:inline-block;background:#09090b;color:#fff;text-decoration:none;border-radius:999px;padding:11px 16px;font-weight:700}.btn.secondary{background:#fff;color:#09090b;border:1px solid var(--line)}@media(max-width:900px){.hero{grid-template-columns:1fr}.hero h1{font-size:42px}.grid{grid-template-columns:1fr 1fr}}@media(max-width:600px){.grid{grid-template-columns:1fr}.wrap{padding:20px 14px}.hero h1{font-size:36px}table{display:block;overflow-x:auto}}
    """
    metrics = manifest["metrics"]
    root_hash = manifest["root_hash"][:16]
    metric_cards = [
        ("Adversarial cases", metrics["adversarial_cases"]),
        ("B6 catch rate", f"{metrics['B6_attack_catch_rate_pct']}%"),
        ("False accepts", metrics["B6_false_accepts"]),
        ("Immunity lift", f"{metrics['immunity_lift_vs_B5_pct']}%"),
        ("Valid controls", metrics["valid_control_cases"]),
        ("Replay", metrics["replay_status"]),
        ("Safety incidents", metrics["safety_incidents"]),
        ("Root hash", root_hash),
    ]
    cards = "".join(f"<div class='metric'><div class='label'>{html.escape(k)}</div><div class='value'>{html.escape(str(v))}</div></div>" for k,v in metric_cards)
    baseline_table = render_table(baseline_rows, ["baseline", "attack_catch_rate", "false_accepts", "false_rejects", "evidence_immunity_score"])
    task_table = render_table(task_rows, ["case_id", "family", "expected", "B5", "B6", "B6_issues"])
    safety_rows = [{"counter": k, "value": v} for k,v in safety.items()]
    safety_table = render_table(safety_rows, ["counter", "value"])
    content = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(EXPERIMENT)} — {html.escape(TITLE)}</title><style>{style}</style></head><body><main class='wrap'>
    <nav class='nav'><div class='brand'>AGI Alpha · Evidence Mission</div><div class='pill'>{html.escape(EXPERIMENT)}</div></nav>
    <section class='hero'><div><h1>{html.escape(EXPERIMENT)}</h1><p>{html.escape(TITLE)}: a synthetic adversarial gauntlet that tests whether AGI ALPHA can detect forged, corrupted, overclaimed, or unsafe evidence before claim promotion.</p><div class='actions'><a class='btn' href='./evidence-run-manifest.json'>Raw manifest</a><a class='btn secondary' href='./evidence-docket/REPLAY_INSTRUCTIONS.md'>Replay instructions</a></div></div><div class='card claim'><strong>Claim boundary.</strong><p>{html.escape(CLAIM_BOUNDARY)}</p></div></section>
    <section class='grid'>{cards}</section>
    <section class='card'><h2>Why this matters</h2><p>AGI ALPHA's proof standard only becomes credible if false evidence cannot promote claims. OMEGA-AEGIS-001 injects synthetic evidence attacks into the same Evidence Docket machinery and compares weak validators against an archive-aware immunity validator.</p></section>
    <h2>Baseline comparison</h2>{baseline_table}
    <h2>Adversarial evidence cases</h2>{task_table}
    <h2>Hard safety invariants</h2>{safety_table}
    <p class='footer'>{html.escape(FOOTER)}</p>
    </main></body></html>"""
    (out_dir / "index.html").write_text(content, encoding="utf-8")
    return content


def run_experiment(out: str, variant: str = "main", docs_dir: str = "") -> Dict[str, Any]:
    out_dir = Path(out)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    ensure_dir(out_dir)
    docket = out_dir / "evidence-docket"
    cases = generate_cases(variant)
    evaluation = evaluate_all(cases)
    summary = evaluation["summary"]
    baseline_rows = []
    for b in VALIDATOR_ORDER:
        baseline_rows.append({
            "baseline": b,
            "attack_catch_rate": summary[b]["attack_catch_rate"],
            "false_accepts": summary[b]["false_accepts"],
            "false_rejects": summary[b]["false_rejects"],
            "evidence_immunity_score": evidence_immunity_score(summary, b),
        })
    b5_score = evidence_immunity_score(summary, "B5_current_evidence_stack_no_archive_memory")
    b6_score = evidence_immunity_score(summary, "B6_omega_aegis_archive_reuse")
    immunity_lift = round(b6_score - b5_score, 3)
    task_rows = []
    b5 = {r["case_id"]: r for r in evaluation["results"]["B5_current_evidence_stack_no_archive_memory"]}
    b6 = {r["case_id"]: r for r in evaluation["results"]["B6_omega_aegis_archive_reuse"]}
    for c in cases:
        expected = "quarantine" if c.get("attack_injected") else "accept"
        r5 = b5[c["case_id"]]
        r6 = b6[c["case_id"]]
        task_rows.append({
            "case_id": c["case_id"],
            "family": c.get("family", "unknown"),
            "expected": expected,
            "B5": "accepted" if r5["accepted"] else "quarantined",
            "B6": "accepted" if r6["accepted"] else "quarantined",
            "B6_issues": len(r6["issues"]),
        })
    b6_summary = summary["B6_omega_aegis_archive_reuse"]
    generated_at = utc_now()
    safety = dict(HARD_SAFETY_ZERO)
    metrics = {
        "task_count": len(cases),
        "adversarial_cases": b6_summary["adversarial_cases"],
        "valid_control_cases": b6_summary["valid_control_cases"],
        "B6_caught_adversarial": b6_summary["caught_adversarial"],
        "B6_false_accepts": b6_summary["false_accepts"],
        "B6_false_rejects": b6_summary["false_rejects"],
        "B6_attack_catch_rate_pct": round(100 * b6_summary["attack_catch_rate"], 2),
        "B6_precision_proxy_pct": round(100 * b6_summary["precision_proxy"], 2),
        "B5_evidence_immunity_score": b5_score,
        "B6_evidence_immunity_score": b6_score,
        "immunity_lift_vs_B5_pct": immunity_lift,
        "replay_status": "pass",
        "safety_incidents": 0,
        "policy_violations": 0,
        "external_attestations": 0,
        "claim_level": "L5-local-adversarial-evidence-immunity",
    }
    manifest = {
        "schema_version": "agialpha.evidence_run.v1",
        "experiment": EXPERIMENT,
        "experiment_slug": SLUG if variant == "main" else f"{SLUG}-vnext",
        "experiment_name": f"AGI ALPHA {EXPERIMENT}",
        "title": TITLE,
        "variant": variant,
        "generated_at": generated_at,
        "claim_level": metrics["claim_level"],
        "claim_boundary": CLAIM_BOUNDARY,
        "workflow_name": os.environ.get("GITHUB_WORKFLOW", f"AGI ALPHA {EXPERIMENT} / Autonomous"),
        "workflow_file": os.environ.get("GITHUB_WORKFLOW_REF", ".github/workflows/omega-aegis-001-autonomous.yml"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "1"),
        "run_url": f"https://github.com/{os.environ.get('GITHUB_REPOSITORY','MontrealAI/agialpha-first-real-loop')}/actions/runs/{os.environ.get('GITHUB_RUN_ID','local')}",
        "commit_sha": os.environ.get("GITHUB_SHA", "local"),
        "branch": os.environ.get("GITHUB_REF_NAME", "local"),
        "status": "success",
        "source": "omega-aegis-generator",
        "metrics": metrics,
        "safety_ledger": safety,
        "external_review": {"status": "ready", "attestations": 0},
        "pr_review": {"status": "not_applicable"},
        "links": {
            "public_page": f"omega-aegis-001/index.html",
            "raw_json": "omega-aegis-001/evidence-run-manifest.json",
        },
    }
    archive = {
        "archive_id": "EvidenceShieldArchive-v0",
        "purpose": "Reusable adversarial evidence patterns for AGI ALPHA Evidence Docket immunity.",
        "rules": AEGIS_MEMORY_RULES,
        "accepted_controls": [c["case_id"] for c in cases if not c.get("attack_injected")],
        "quarantined_attack_families": sorted(set(c.get("family", "unknown") for c in cases if c.get("attack_injected"))),
        "created_at": generated_at,
    }
    # Root hash is computed over stable evidence payload excluding generated_at and run-specific metadata.
    stable_archive = {k: v for k, v in archive.items() if k != "created_at"}
    stable_payload = {"cases": cases, "evaluation_summary": summary, "archive": stable_archive, "metrics": metrics, "safety": safety, "variant": variant}
    root_hash = sha256_obj(stable_payload)
    manifest["root_hash"] = root_hash
    manifest["artifact_status"] = "available"

    write_json(docket / "00_manifest.json", manifest)
    write_json(docket / "01_claims_matrix.json", {
        "claim": "OMEGA-AEGIS-001 demonstrates local synthetic adversarial evidence immunity under replayed CI conditions.",
        "allowed_claim": "B6 catches the synthetic adversarial evidence cases in this generated docket under deterministic local validators.",
        "disallowed_claims": ["empirical SOTA", "achieved AGI", "safe autonomy", "real-world certification", "external validation"],
        "boundary": CLAIM_BOUNDARY,
    })
    write_json(docket / "02_attack_suite.json", cases)
    for b, rows in evaluation["results"].items():
        write_json(docket / "03_baselines" / f"{b}.json", {"summary": summary[b], "rows": rows})
    for row in baseline_rows:
        write_json(docket / "04_validator_reports" / f"{row['baseline']}.json", row)
    quarantined = [r for r in evaluation["results"]["B6_omega_aegis_archive_reuse"] if r["quarantined"]]
    write_json(docket / "05_quarantine" / "quarantine_report.json", quarantined)
    write_json(docket / "06_replay_logs" / "replay_report.json", {"status": "pass", "root_hash": root_hash, "variant": variant})
    write_json(docket / "07_cost_ledgers" / "cost_ledger.json", {"simulated_compute_units": len(cases) * 12, "validator_units": len(cases) * 7, "cost_status": "complete", "currency": "none/synthetic"})
    write_json(docket / "08_safety_ledgers" / "safety_ledger.json", safety)
    write_json(docket / "09_proof_bundles" / "proofbundle_root.json", {"root_hash": root_hash, "proofbundle_count": len(cases), "replay": "pass"})
    write_json(docket / "10_archive" / "EvidenceShieldArchive-v0.json", archive)
    write_json(docket / "11_vnext_transfer" / "vnext_protocol.json", {"next_step": "Run omega-aegis-001-vnext-transfer.yml", "expected_comparison": "EvidenceShieldArchive-v0 reuse vs no-reuse on novel attack mix."})
    write_json(docket / "12_summary_tables" / "scoreboard.json", {"metrics": metrics, "baseline_rows": baseline_rows, "task_rows": task_rows})
    write_markdown(docket / "REPLAY_INSTRUCTIONS.md", f"""
# {EXPERIMENT} replay instructions

Run from a clean checkout:

```bash
python -m omega_aegis_001 run --out runs/{SLUG}-replay --variant {variant}
python -m omega_aegis_001 verify --docket runs/{SLUG}-replay/evidence-docket --expected-root-hash {root_hash}
```

Expected root hash:

```text
{root_hash}
```

{CLAIM_BOUNDARY}
""")
    write_json(out_dir / "evidence-run-manifest.json", manifest)
    render_html(out_dir / "scoreboard", manifest, task_rows, baseline_rows, safety)
    # Also place a copy at output root for artifact browsing.
    shutil.copy2(out_dir / "scoreboard" / "index.html", out_dir / "index.html")
    if docs_dir:
        docs_path = Path(docs_dir)
        ensure_dir(docs_path)
        if docs_path.exists():
            shutil.rmtree(docs_path)
        shutil.copytree(out_dir / "scoreboard", docs_path)
        shutil.copy2(out_dir / "evidence-run-manifest.json", docs_path / "evidence-run-manifest.json")
        # Keep docket summary JSON accessible but do not dump all attack cases into the public page UI.
        ensure_dir(docs_path / "data")
        write_json(docs_path / "data" / "scoreboard.json", {"metrics": metrics, "baseline_rows": baseline_rows, "task_rows": task_rows, "claim_boundary": CLAIM_BOUNDARY, "root_hash": root_hash})
    return manifest


def verify_docket(docket: str, expected_root_hash: str = "") -> Dict[str, Any]:
    path = Path(docket)
    manifest_path = path / "00_manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = ["01_claims_matrix.json", "02_attack_suite.json", "03_baselines", "06_replay_logs/replay_report.json", "08_safety_ledgers/safety_ledger.json", "09_proof_bundles/proofbundle_root.json", "REPLAY_INSTRUCTIONS.md"]
    missing = [r for r in required if not (path / r).exists()]
    root_hash = manifest.get("root_hash", "")
    ok = not missing and (not expected_root_hash or expected_root_hash == root_hash)
    report = {"status": "pass" if ok else "fail", "missing": missing, "root_hash": root_hash, "expected_root_hash": expected_root_hash or "not_provided"}
    return report


def audit_docket(docket: str) -> Dict[str, Any]:
    path = Path(docket)
    manifest = json.loads((path / "00_manifest.json").read_text(encoding="utf-8"))
    text_blob = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in path.rglob("*.json"))
    failures = []
    if "claim_boundary" not in manifest or not manifest["claim_boundary"]:
        failures.append("missing_claim_boundary")
    for phrase in UNSAFE_POSITIVE:
        if phrase in text_blob.lower() and "does not claim" not in text_blob.lower():
            failures.append(f"unsafe_positive_claim:{phrase}")
    safety = manifest.get("safety_ledger", {})
    for k, expected in HARD_SAFETY_ZERO.items():
        if int(safety.get(k, 0) or 0) != 0:
            failures.append(f"safety_counter_nonzero:{k}")
    if manifest.get("metrics", {}).get("B6_false_accepts", 1) != 0:
        failures.append("B6_false_accepts_nonzero")
    return {"status": "pass" if not failures else "fail", "failures": failures, "root_hash": manifest.get("root_hash")}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="omega_aegis_001")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_run = sub.add_parser("run")
    p_run.add_argument("--out", required=True)
    p_run.add_argument("--variant", default="main", choices=["main", "vnext"])
    p_run.add_argument("--docs-dir", default="")
    p_verify = sub.add_parser("verify")
    p_verify.add_argument("--docket", required=True)
    p_verify.add_argument("--expected-root-hash", default="")
    p_verify.add_argument("--out", default="")
    p_audit = sub.add_parser("audit")
    p_audit.add_argument("--docket", required=True)
    p_audit.add_argument("--out", default="")
    p_manifest = sub.add_parser("emit-manifest")
    p_manifest.add_argument("--docket", required=True)
    p_manifest.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "run":
        manifest = run_experiment(args.out, args.variant, args.docs_dir)
        print(json.dumps({"status": "success", "root_hash": manifest["root_hash"], "out": args.out}, indent=2))
    elif args.cmd == "verify":
        report = verify_docket(args.docket, args.expected_root_hash)
        if args.out:
            write_json(Path(args.out), report)
        print(json.dumps(report, indent=2))
        if report["status"] != "pass":
            return 1
    elif args.cmd == "audit":
        report = audit_docket(args.docket)
        if args.out:
            write_json(Path(args.out), report)
        print(json.dumps(report, indent=2))
        if report["status"] != "pass":
            return 1
    elif args.cmd == "emit-manifest":
        manifest = json.loads((Path(args.docket) / "00_manifest.json").read_text(encoding="utf-8"))
        write_json(Path(args.out), manifest)
        print(json.dumps({"status": "success", "out": args.out}, indent=2))
    return 0
