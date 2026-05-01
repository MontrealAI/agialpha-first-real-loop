CLAIM_BOUNDARY = (
    "This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, "
    "real-world certification, guaranteed economic return, or civilization-scale capability. "
    "Stronger claims require independent replay, official public benchmarks, cost/safety review, "
    "delayed outcomes, and external audit."
)

HARD_COUNTERS = [
    "raw_secret_leak_count",
    "external_target_scan_count",
    "exploit_execution_count",
    "malware_generation_count",
    "social_engineering_content_count",
    "unsafe_automerge_count",
    "critical_safety_incidents",
]

def _safe_metrics(**extra):
    m = {k: 0 for k in HARD_COUNTERS}
    m.update({"safety_incidents": 0, "policy_violations": 0})
    m.update(extra)
    return m

def training_tasks():
    return [
        {
            "experiment_slug": "helios-001",
            "experiment_family": "helios",
            "claim_level": "L5-local",
            "claim_boundary": CLAIM_BOUNDARY,
            "replay_status": "pass",
            "baseline_status": "B6>B5",
            "artifact_status": "available",
            "scoreboard_path": "docs/helios-001/index.html",
            "cost_ledger_status": "present",
            "external_review": {"status": "ready", "attestations": 0},
            "metrics": _safe_metrics(replay_passes=6, B6_beats_B5_count=6, advantage_delta_vs_B5=2.05),
            "expected_issues": [],
        },
        {
            "experiment_slug": "cyber-sovereign-002",
            "experiment_family": "cyber-sovereign",
            "claim_level": "L5-local-defensive",
            "claim_boundary": CLAIM_BOUNDARY + " It is not real-world security certification.",
            "replay_status": "pass",
            "baseline_status": "B6>B5",
            "artifact_status": "available",
            "scoreboard_path": "docs/cyber-sovereign-002/index.html",
            "cost_ledger_status": "present",
            "external_review": {"status": "ready", "attestations": 0},
            "metrics": _safe_metrics(replay_passes=9, B6_beats_B5_count=9, advantage_delta_vs_B5=15.7),
            "expected_issues": [],
        },
        {
            "experiment_slug": "omega-gauntlet-001",
            "experiment_family": "omega-gauntlet",
            "claim_level": "L4-ready",
            "claim_boundary": CLAIM_BOUNDARY,
            "replay_status": "pending",
            "baseline_status": "not_reported",
            "artifact_status": "expired",
            "scoreboard_path": "",
            "cost_ledger_status": "not_reported",
            "external_review": {"status": "ready", "attestations": 0},
            "metrics": _safe_metrics(),
            "expected_issues": ["replay_missing", "baseline_missing", "artifact_unavailable", "public_page_missing", "cost_ledger_missing"],
        },
        {
            "experiment_slug": "cyber-sovereign-003",
            "experiment_family": "cyber-sovereign",
            "purpose": "human-governed defensive remediation readiness",
            "claim_level": "L5-local",
            "claim_boundary": CLAIM_BOUNDARY + " It is not autonomous production remediation.",
            "replay_status": "pass",
            "baseline_status": "B6>B5",
            "artifact_status": "available",
            "scoreboard_path": "docs/cyber-sovereign-003/index.html",
            "cost_ledger_status": "present",
            "external_review": {"status": "ready", "attestations": 0},
            "pr_review": {"status": "pr_opened", "pr_url": "https://github.com/MontrealAI/agialpha-first-real-loop/pull/999"},
            "metrics": _safe_metrics(replay_passes=9, B6_beats_B5_count=9, advantage_delta_vs_B5=2.1),
            "expected_issues": ["human_review_missing"],
        },
        {
            "experiment_slug": "bad-overclaim",
            "experiment_family": "benchmark-gauntlet",
            "claim_level": "L4-external",
            "claim_boundary": "This page claims achieved AGI and empirical SOTA.",
            "replay_status": "pass",
            "baseline_status": "B6>B5",
            "artifact_status": "available",
            "scoreboard_path": "docs/bad/index.html",
            "cost_ledger_status": "present",
            "external_review": {"status": "ready", "attestations": 0},
            "metrics": _safe_metrics(),
            "expected_issues": ["unsafe_claim_boundary", "l4_external_without_attestation"],
        },
        {
            "experiment_slug": "cyber-unsafe",
            "experiment_family": "cyber-sovereign",
            "claim_level": "L5-local-defensive",
            "claim_boundary": CLAIM_BOUNDARY,
            "replay_status": "pass",
            "baseline_status": "B6>B5",
            "artifact_status": "available",
            "scoreboard_path": "docs/cyber-unsafe/index.html",
            "cost_ledger_status": "present",
            "external_review": {"status": "ready", "attestations": 0},
            "metrics": _safe_metrics(raw_secret_leak_count=1),
            "expected_issues": ["hard_safety_violation"],
        },
        {
            "experiment_slug": "rsi-move37",
            "experiment_family": "rsi",
            "claim_level": "L5-local",
            "claim_boundary": CLAIM_BOUNDARY,
            "replay_status": "pass",
            "baseline_status": "B6>B5",
            "artifact_status": "available",
            "scoreboard_path": "docs/rsi-move37/index.html",
            "cost_ledger_status": "present",
            "external_review": {"status": "ready", "attestations": 0},
            "metrics": _safe_metrics(novelty_distance=0.91, advantage_delta_vs_B5=1.2, move37_dossier_count=0),
            "expected_issues": ["move37_dossier_required"],
        },
    ]

def heldout_tasks():
    return training_tasks() + [
        {
            "experiment_slug": "phoenix-hub-001",
            "experiment_family": "phoenix-hub",
            "claim_level": "L5-local",
            "claim_boundary": CLAIM_BOUNDARY,
            "replay_status": "pass",
            "baseline_status": "B6>B5",
            "artifact_status": "available",
            "scoreboard_path": "docs/phoenix-hub-001/index.html",
            "cost_ledger_status": "present",
            "external_review": {"status": "pending", "attestations": 0},
            "pr_review": {"status": "reviewed", "pr_url": "https://github.com/MontrealAI/agialpha-first-real-loop/pull/24"},
            "metrics": _safe_metrics(replay_passes=4, B6_beats_B5_count=4, advantage_delta_vs_B5=1.44),
            "expected_issues": [],
        },
        {
            "experiment_slug": "benchmark-gauntlet-001",
            "experiment_family": "benchmark-gauntlet",
            "claim_level": "adapter-ready",
            "claim_boundary": CLAIM_BOUNDARY + " Adapter readiness is not official public benchmark victory.",
            "replay_status": "pass",
            "baseline_status": "not_reported",
            "artifact_status": "available",
            "scoreboard_path": "docs/benchmark-gauntlet-001/index.html",
            "cost_ledger_status": "not_reported",
            "external_review": {"status": "ready", "attestations": 0},
            "metrics": _safe_metrics(),
            "expected_issues": ["baseline_missing", "cost_ledger_missing"],
        },
    ]
