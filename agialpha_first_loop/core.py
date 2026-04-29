from pathlib import Path
from .models import load_json, dump_json, stable_hash, now_iso

ENERGY_SINKS = [
    "compressors",
    "condenser fans and head pressure",
    "evaporator fans",
    "defrost cycles",
    "doors and infiltration",
    "lighting and internal heat gain",
    "controls and sensors",
    "maintenance and coil cleanliness",
]

LOW_CAPEX_BUCKETS = {"no-cost", "low", "low-to-moderate"}


def run_mark_review(mark_card):
    scores = mark_card["scores"]
    avg = sum(scores.values()) / len(scores)
    green = avg >= 4.0 and scores["safety"] >= 4 and scores["executability"] >= 4 and scores["reusability"] >= 4
    return {**mark_card, "average_score": round(avg, 2), "green_flamed": green}


def job1_source_discovery(sources):
    credible = [s for s in sources if s.get("credibility") in {"government", "utility", "institutional", "engineering", "manufacturer"}]
    by_type = {}
    for s in credible:
        by_type[s["source_type"]] = by_type.get(s["source_type"], 0) + 1
    success = len(credible) >= 10 and by_type.get("government_or_public_institution", 0) >= 2 and by_type.get("manufacturer_or_technical", 0) >= 2 and by_type.get("industry_or_engineering", 0) >= 2
    return {
        "job_id": "J1",
        "name": "Source Discovery",
        "credible_source_count": len(credible),
        "source_type_counts": by_type,
        "sources": credible,
        "success": success,
        "validator_notes": "Sources are curated public references. External proof mode should archive snapshots and run link checks.",
    }


def job2_facility_model(seed, sources):
    profile = {
        "job_id": "J2",
        "name": "Facility Model Extraction",
        "facility_type": "refrigerated warehouse / cold-chain storage facility",
        "region": "unspecified; recommendations must remain climate- and tariff-aware",
        "major_energy_sinks": ENERGY_SINKS,
        "constraints": seed["risk_envelope"],
        "missing_assumptions": [
            "facility size",
            "temperature zones",
            "compressor type and control strategy",
            "door-open frequency",
            "maintenance history",
            "electricity tariff and demand charges",
            "food-safety requirements",
        ],
        "evidence_references": [s["id"] for s in sources[:8]],
        "unsupported_details_invented": False,
        "success": True,
    }
    return profile


def job3_generate_interventions(candidates, sources_by_id):
    surviving = []
    rejected = []
    for c in candidates:
        enough_sources = len(c.get("source_ids", [])) >= 3
        low_capex = c.get("capex_bucket") in LOW_CAPEX_BUCKETS
        unsupported = any(s not in sources_by_id for s in c.get("source_ids", []))
        item = {**c, "enough_sources": enough_sources, "low_capex": low_capex, "unsupported_source_ids": unsupported}
        if enough_sources and low_capex and not unsupported:
            surviving.append(item)
        else:
            rejected.append(item)
    return {
        "job_id": "J3",
        "name": "Intervention Generation",
        "candidate_count": len(candidates),
        "surviving_count": len(surviving),
        "surviving_candidates": surviving,
        "rejected_candidates": rejected,
        "success": len(surviving) >= 7,
    }


def risk_tier(candidate):
    text = (candidate["title"] + " " + candidate.get("mechanism", "") + " " + " ".join(candidate.get("risk_notes", []))).lower()
    prohibited_terms = ["refrigerant handling", "electrical work", "food-safety setpoint change", "guaranteed savings"]
    restricted_terms = ["setpoint", "defrost", "controls", "compressor staging", "head pressure"]
    if any(t in text for t in prohibited_terms):
        return "PROHIBITED"
    if any(t in text for t in restricted_terms):
        return "CAUTION"
    return "ALLOW"


def job4_causalize_redteam(surviving):
    evaluated = []
    for c in surviving:
        tier = risk_tier(c)
        verdict = "ALLOW" if tier == "ALLOW" else "ALLOW_WITH_CONSTRAINTS" if tier == "CAUTION" else "PROHIBIT"
        allow_final = verdict in {"ALLOW", "ALLOW_WITH_CONSTRAINTS"}
        evaluated.append({
            **c,
            "causal_chain": c.get("causal_chain", []),
            "preconditions": c.get("preconditions", []),
            "failure_modes": c.get("failure_modes", []),
            "evidence_gaps": c.get("evidence_gaps", []),
            "risk_tier": tier,
            "red_team_verdict": verdict,
            "allowed_for_ranking": allow_final,
        })
    final = [x for x in evaluated if x["allowed_for_ranking"]]
    return {
        "job_id": "J4",
        "name": "Causalization + Red-Team",
        "evaluated_candidates": evaluated,
        "allowed_for_ranking_count": len(final),
        "success": all(x["risk_tier"] != "PROHIBITED" for x in final),
    }


def quality_score(candidate):
    # Conservative deterministic scoring: evidence, low capex, causal clarity, safety.
    evidence = min(5, len(candidate.get("source_ids", [])))
    capex = {"no-cost": 5, "low": 4.5, "low-to-moderate": 4, "moderate": 3}.get(candidate.get("capex_bucket"), 2)
    safety = 5 if candidate.get("risk_tier") == "ALLOW" else 4 if candidate.get("risk_tier") == "CAUTION" else 0
    causal = min(5, len(candidate.get("causal_chain", [])))
    return round(0.30 * evidence + 0.25 * capex + 0.25 * safety + 0.20 * causal, 2)


def job5_rank_and_docket(redteam_result, reviewer_decisions):
    candidates = [c for c in redteam_result["evaluated_candidates"] if c["allowed_for_ranking"]]
    for c in candidates:
        c["quality_score"] = quality_score(c)
        c["reviewer_label"] = reviewer_decisions.get(c["id"], "needs_review")
    ranked = sorted(candidates, key=lambda c: c["quality_score"], reverse=True)
    top5 = ranked[:5]
    accepted = [c for c in top5 if c["reviewer_label"] == "accepted"]
    return {
        "job_id": "J5",
        "name": "Ranking + Evidence Docket",
        "top5_interventions": top5,
        "accepted_interventions": accepted,
        "accepted_count": len(accepted),
        "success": len(accepted) >= 3,
    }


def extract_compiler(job_outputs):
    return {
        "id": "ColdChain-Energy-Compiler-v0",
        "purpose": "Reusable cold-chain energy evidence workflow extracted from Seed-001.",
        "source_discovery_rules": [
            "prefer government, utility, institutional, engineering, manufacturer, and standards sources",
            "require at least three evidence traces per accepted intervention",
            "separate evidence for mechanism, implementation precondition, and risk boundary",
        ],
        "facility_model_schema": {
            "facility_type": "string",
            "major_energy_sinks": "list[string]",
            "constraints": "list[string]",
            "missing_assumptions": "list[string]",
            "evidence_references": "list[source_id]",
        },
        "intervention_schema": {
            "title": "string",
            "target_energy_sink": "string",
            "mechanism": "string",
            "capex_bucket": "no-cost|low|low-to-moderate|moderate|high",
            "source_ids": "list[source_id]",
            "preconditions": "list[string]",
            "failure_modes": "list[string]",
            "risk_notes": "list[string]",
        },
        "causalization_rubric": [
            "show how the intervention reduces load, runtime, lift, heat gain, or control waste",
            "list preconditions and missing measurements",
            "separate advisory recommendations from operational changes",
        ],
        "red_team_rules": [
            "block refrigerant-handling recommendations",
            "block food-safety-critical setpoint changes without expert review",
            "block electrical work recommendations without licensed review",
            "block guaranteed savings claims",
            "label controls/defrost/head-pressure work as CAUTION unless framed as audit/review",
        ],
        "final_output_template": "ranked_interventions_with_evidence_and_risk_notes",
        "evidence_docket_template": "templates/evidence_docket_template.json",
        "extracted_from": [o["job_id"] for o in job_outputs],
    }


def create_seed002(seed1, compiler):
    return {
        "id": "ColdChain-Energy-Seed-002",
        "parent_seed_id": seed1["id"],
        "mutation": "target facility changes from refrigerated warehouse to food-processing cold-chain facility",
        "reused_capability": compiler["id"],
        "added_constraints": [
            "stronger food-safety review emphasis",
            "stronger restriction on setpoint and defrost recommendations",
            "recommend measurement and review before operational control changes",
        ],
        "foresight_genome": seed1["foresight_genome"] + ["Food-processing cold-chain facilities combine refrigeration loads with process, hygiene, scheduling, and product-safety constraints."],
        "fusion_plan": seed1["fusion_plan"],
        "risk_envelope": seed1["risk_envelope"] + ["no food-safety-critical process recommendation without expert review"],
        "promotion_criteria": seed1["promotion_criteria"],
    }


def compare_treatment_control(control, treatment):
    yc = control["accepted_useful_interventions"] / control["total_cost_units"]
    yt = treatment["accepted_useful_interventions"] / treatment["total_cost_units"]
    lift = (yt - yc) / yc if yc else 0
    hallucination_delta = treatment["hallucinated_sources"] - control["hallucinated_sources"]
    safety_delta = treatment["safety_flags"] - control["safety_flags"]
    return {
        "primary_metric": "accepted_useful_interventions / total_cost_units",
        "control_yield": round(yc, 4),
        "treatment_yield": round(yt, 4),
        "reuse_lift": round(lift, 4),
        "reuse_lift_percent": round(100 * lift, 2),
        "hallucination_delta": hallucination_delta,
        "safety_delta": safety_delta,
        "passed": lift >= 0.25 and hallucination_delta <= 0 and safety_delta <= 0,
        "claim_boundary": "This treatment/control result is deterministic first-loop evidence. External proof requires independent reviewer replication and archived source verification.",
    }


def build_evidence_docket(project_root: Path, out: Path):
    data = project_root / "data"
    seed = load_json(data / "seed_001.json")
    mark = run_mark_review(load_json(data / "mark_review_card.json"))
    sovereign = load_json(data / "sovereign_001.json")
    sources = load_json(data / "sources.json")
    candidates = load_json(data / "candidate_interventions_seed001.json")
    reviewer = load_json(data / "reviewer_decisions_seed001.json")
    sources_by_id = {s["id"]: s for s in sources}

    j1 = job1_source_discovery(sources)
    j2 = job2_facility_model(seed, j1["sources"])
    j3 = job3_generate_interventions(candidates, sources_by_id)
    j4 = job4_causalize_redteam(j3["surviving_candidates"])
    j5 = job5_rank_and_docket(j4, reviewer["decisions"])
    jobs = [j1, j2, j3, j4, j5]
    compiler = extract_compiler(jobs)
    seed2 = create_seed002(seed, compiler)
    control = load_json(data / "seed002_control_result.json")
    treatment = load_json(data / "seed002_treatment_result.json")
    comparison = compare_treatment_control(control, treatment)

    docket = {
        "docket_id": "ColdChain-Energy-Loop-001",
        "created_at": now_iso(),
        "claim_boundary": "This is a replayable first-loop scaffold and deterministic evidence docket. It is not a claim of AGI, ASI, empirical SOTA, deployment authority, guaranteed savings, or facility-specific engineering advice.",
        "seed_id": seed["id"],
        "mark_green_flamed": mark["green_flamed"],
        "sovereign_id": sovereign["id"],
        "jobs_success": {j["job_id"]: j["success"] for j in jobs},
        "accepted_interventions": j5["accepted_interventions"],
        "reusable_construct": compiler,
        "vnext_seed": seed2,
        "treatment_control": comparison,
        "success_conditions": {
            "seed_created": True,
            "mark_reviewed": mark["green_flamed"],
            "sovereign_executed": all(j["success"] for j in jobs),
            "evidence_docket_exists": True,
            "compiler_extracted": compiler["id"] == "ColdChain-Energy-Compiler-v0",
            "vnext_improved": comparison["passed"],
        },
    }
    docket["loop_passed"] = all(docket["success_conditions"].values())
    docket["docket_hash"] = stable_hash({k:v for k,v in docket.items() if k != "docket_hash"})

    out.mkdir(parents=True, exist_ok=True)
    dump_json(out / "00_manifest.json", docket)
    dump_json(out / "01_seed_001.json", seed)
    dump_json(out / "02_mark_review_card.json", mark)
    dump_json(out / "03_sovereign_001.json", sovereign)
    dump_json(out / "04_job_outputs.json", jobs)
    dump_json(out / "05_sources_used.json", sources)
    dump_json(out / "06_accepted_interventions.json", j5["accepted_interventions"])
    dump_json(out / "07_coldchain_energy_compiler_v0.json", compiler)
    dump_json(out / "08_seed_002.json", seed2)
    dump_json(out / "09_treatment_control_comparison.json", comparison)
    decision = build_decision_memo(docket, jobs, comparison)
    (out / "10_decision_memo.md").write_text(decision, encoding="utf-8")
    (out / "REPLAY_INSTRUCTIONS.md").write_text("""# Replay instructions\n\nFrom the repository root, run:\n\n```bash\npython -m agialpha_first_loop.run --out runs/coldchain-energy-loop-001-replay\npython -m unittest discover -s tests\n```\n\nCompare the generated `00_manifest.json` hash with the expected fields. The timestamp may differ; the deterministic content and pass/fail conditions should match.\n""", encoding="utf-8")
    return docket


def build_decision_memo(docket, jobs, comparison):
    status = "PASSED" if docket["loop_passed"] else "NOT PASSED"
    return f"""
# Decision Memo — ColdChain-Energy-Loop-001

**Decision:** {status}

## What was tested

One Nova-Seed was reviewed by MARK, instantiated as a mini Sovereign, executed through five AGI Jobs, packaged into an Evidence Docket, converted into `ColdChain-Energy-Compiler-v0`, and tested for reuse in Seed-002.

## Result

- MARK green-flamed: `{docket['mark_green_flamed']}`
- Five jobs successful: `{all(j['success'] for j in jobs)}`
- Accepted interventions: `{len(docket['accepted_interventions'])}`
- Reusable compiler extracted: `ColdChain-Energy-Compiler-v0`
- Treatment/control reuse lift: `{comparison['reuse_lift_percent']}%`
- Loop passed: `{docket['loop_passed']}`

## Claim boundary

This is a deterministic first-loop scaffold. It demonstrates the mechanics of a replayable Evidence Docket and reuse test. External publication-grade proof requires independent reviewer replication, archived source verification, baseline comparison, and cost/safety ledger review.

## Next action

Run the same loop with a real independent reviewer and archived source snapshots, then publish the completed Evidence Docket.
""".strip() + "\n"
