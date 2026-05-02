from __future__ import annotations
import json
from pathlib import Path


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def disclaimer():
    return "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."


def run_replay(docket: Path):
    required = [
        docket / "evidence-run-manifest.json",
        docket / "28_summary_tables/scoreboard.json",
        docket / "04_alpha_agi_insight/insight_report.json",
    ]
    missing = [str(p) for p in required if not p.exists()]
    report_path = docket / "17_replay_logs/replay_report.json"
    if missing:
        write_json(report_path, {
            "status": "fail",
            "reason": "missing_required_evidence",
            "missing_paths": missing,
            "claim_boundary": disclaimer(),
        })
        return {"status": "fail", "missing_paths": missing}

    write_json(report_path, {
        "status": "pass",
        "validated_artifacts": [str(p) for p in required],
        "claim_boundary": disclaimer(),
    })
    return {"status": "pass"}
