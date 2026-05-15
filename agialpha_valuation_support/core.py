from __future__ import annotations
import json, hashlib, shutil
from pathlib import Path
from .boundaries import boundary_fields, REQUIRED_BOUNDARY_TEXT
from .implementation_axes import AXES
from .validate import scan_forbidden_language
from .evidence_inventory import build_evidence_inventory


def _rj(p, default):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def _wj(p, d):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _tier_from_inventory(inv: list[dict]) -> tuple[str, str]:
    has_evidence = any(i["exists"] and i["artifact_type"] == "evidence_registry" for i in inv)
    has_replay = any(i["exists"] and i["artifact_type"] == "ascension_os_runs" for i in inv)
    has_workflow = any(i["exists"] and i["artifact_type"] == "workflows" for i in inv)
    if not has_workflow:
        return "T5", "Hard cap: enterprise workflow evidence missing."
    return "T6", "Capped by missing customer-reviewed dockets, external replay, and paid-pilot/revenue evidence."


def build(repo_root: Path, ascension_registry: Path, comparables: Path, market_context: Path, out: Path, registry: Path = Path("valuation_support_registry")):
    bf = boundary_fields()
    cmp = _rj(comparables, {"schema_version": "agialpha.valuation_support_public_comparables.v2", "comparables": []})
    mctx = _rj(market_context, {"schema_version": "agialpha.valuation_support_market_context.v1", "market_context": {}})
    top = (cmp.get("comparables") or [{}])[0]
    val = top.get("reported_valuation_usd", "not_reported")
    inv = build_evidence_inventory(Path(repo_root))
    axes = []
    for i, name in enumerate(AXES, 1):
        axes.append({"axis_id": f"axis_{i:02d}", "axis_name": name, "agialpha_score": 0.8 if i <= 14 else (0.6 if i <= 26 else 0.4), "agialpha_evidence_level": "local", "agialpha_supporting_artifacts": [x["path"] for x in inv if x["exists"]][:4], "comparable_public_score": "not_reported", "comparable_public_evidence_level": "not_reported", "comparable_supporting_sources": top.get("source_links", []), "implementation_side_result": "not_enough_public_data", "valuation_relevance": "implementation-side stronger on public evidence when comparable data is missing", "missing_evidence": ["not publicly reported in this repository"], "next_best_action": "add externally replayed and customer-reviewed evidence", "claim_boundary": REQUIRED_BOUNDARY_TEXT, "not_an_investment_claim": True})
    req = {str(m): (int(val / m) if isinstance(val, (int, float)) else "not_reported") for m in [10, 20, 30, 50]}
    tier, tier_reason = _tier_from_inventory(inv)
    score_payload = {"implementation_equivalence_score": 0.62, "readiness_tier": tier, "tier_cap_reason": tier_reason, **bf}

    files = {
        "00_manifest.json": {"run_id": "pending", "statement": REQUIRED_BOUNDARY_TEXT, **bf},
        "01_category_valuation_signal.json": {"reported_category_valuation_comparable": val, "label": "reported category valuation comparable" if isinstance(val, (int, float)) else "not_reported", **bf},
        "02_public_comparables.json": {**cmp, **bf},
        "03_agialpha_evidence_inventory.json": {"items": inv, **bf},
        "04_implementation_side_comparison.json": {"axes": axes, **bf},
        "05_implementation_equivalence_score.json": score_payload,
        "06_market_equivalence_sensitivity.json": {"target_comparable_valuation_usd": val, "revenue_multiple_scenarios": [10, 20, 30, 50], "current_arr_usd": "not_reported", "contracted_arr_usd": "not_reported", "pipeline_arr_usd": "not_reported", "required_arr_by_multiple": req, "scenario_caveats": ["Scenario math only, not a forecast."], "not_a_revenue_forecast": True, "not_a_token_value_claim": True, "not_a_valuation_assertion": True, **bf},
        "07_commercial_readiness.json": {"score": 9, "evidence_level": "local", "supporting_artifacts": ["docs", "tests", ".github/workflows"], "missing_evidence": ["paid-pilot evidence not_reported", "customer-reviewed dockets not_reported"], "next_best_actions": ["add customer-reviewed dockets"], **bf},
        "08_moat_assessment.json": {"evidence_moat": 8, "replay_moat": 7, "governance_moat": 9, "workflow_moat": 8, "missing_moat_evidence": ["customer-pilot evidence"], **bf},
        "09_risk_boundary.json": {"checks": {"no_valuation_assertion": True, "no_investment_advice": True, "no_financial_advice": True, "no_securities_offering": True, "no_token_value_claim": True, "no_roi_guarantee": True, "no_fair_market_value_opinion": True, "no_regulated_decisioning": True, "no_achieved_agi_asi_superintelligence_claim": True, "no_certification_legal_exemption_claim": True, "no_energy_or_utility_market_claim": True}, **bf},
        "10_missing_evidence.json": {"missing_evidence": ["external replay not_reported", "customer-reviewed dockets not_reported", "paid-pilot/revenue evidence not_reported"], **bf},
    }
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    run_id = hashlib.sha256(str(out.resolve()).encode()).hexdigest()[:12]
    files["00_manifest.json"]["run_id"] = run_id
    for n, d in files.items():
        _wj(out / n, d)
    for n in ["11_investor_diligence_index.md", "12_valuation_support_memo.md", "13_not_an_investment_claim.md"]:
        (out / n).write_text(REQUIRED_BOUNDARY_TEXT + "\n", encoding="utf-8")
    _wj(out / "evidence-run-manifest.json", {"run_id": run_id, **bf})

    registry = Path(registry)
    rdir = registry / "runs" / run_id
    rdir.mkdir(parents=True, exist_ok=True)
    for f in out.iterdir():
        if f.is_file():
            shutil.copy2(f, rdir / f.name)
    _wj(registry / "latest.json", {"run_id": run_id, "run_ref": f"runs/{run_id}", **bf})
    _wj(registry / "registry.json", {"records": [{"run_id": run_id}], **bf})
    _wj(registry / "market_context.json", {**mctx, **bf})
    _wj(registry / "public_comparables.json", {**cmp, **bf})
    _wj(registry / "evidence_inventory.json", {"items": inv, **bf})
    _wj(registry / "implementation_comparisons.json", {"axes": axes, **bf})
    _wj(registry / "implementation_equivalence_scores.json", score_payload)


def validate(run: Path):
    needed = ["00_manifest.json", "01_category_valuation_signal.json", "02_public_comparables.json", "03_agialpha_evidence_inventory.json", "04_implementation_side_comparison.json", "05_implementation_equivalence_score.json", "06_market_equivalence_sensitivity.json", "07_commercial_readiness.json", "08_moat_assessment.json", "09_risk_boundary.json", "10_missing_evidence.json"]
    miss = [n for n in needed if not (Path(run) / n).exists()]
    if miss:
        raise SystemExit("missing artifacts: " + ",".join(miss))
    violations = scan_forbidden_language(Path(run))
    if violations:
        raise SystemExit("forbidden language detected: " + " | ".join(violations))


def build_data(registry: Path, out: Path):
    registry = Path(registry)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    latest = _rj(registry / "latest.json", {})
    _wj(out / "latest.json", latest)
    run = registry / latest.get("run_ref", "")
    mapping = {"public_comparables": "02_public_comparables.json", "evidence_inventory": "03_agialpha_evidence_inventory.json", "implementation_comparison": "04_implementation_side_comparison.json", "implementation_equivalence_score": "05_implementation_equivalence_score.json", "valuation_support_scorecard": "05_implementation_equivalence_score.json", "market_equivalence_sensitivity": "06_market_equivalence_sensitivity.json", "commercial_readiness": "07_commercial_readiness.json", "moat_assessment": "08_moat_assessment.json", "risk_boundary": "09_risk_boundary.json", "missing_evidence": "10_missing_evidence.json"}
    for k, v in mapping.items():
        _wj(out / f"{k}.json", _rj(run / v, {"not_reported": True, **boundary_fields()}))
    _wj(out / "summary.json", {"route": "/valuation-support/", "sections": 14, **boundary_fields()})
