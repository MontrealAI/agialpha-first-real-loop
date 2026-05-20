from __future__ import annotations

from typing import Any


def compare_archive_reuse(b5: dict[str, Any], b6: dict[str, Any]) -> dict[str, Any]:
    b5_acc = int(b5.get("accepted_task_count", 0))
    b6_acc = int(b6.get("accepted_task_count", 0))
    b5_score = float(b5.get("verified_work_score", 0.0))
    b6_score = float(b6.get("verified_work_score", 0.0))
    delta = round(b6_score - b5_score, 6)
    lift_pct = 0.0 if b5_score == 0 else round((delta / b5_score) * 100.0, 6)
    beats = b6_acc > b5_acc or b6_score > b5_score
    return {
        "B6_beats_B5": beats,
        "B6_advantage_delta_vs_B5": delta,
        "archive_reuse_lift_pct": lift_pct,
        "B5_no_archive_accepted_tasks": b5_acc,
        "B6_archive_reuse_accepted_tasks": b6_acc,
    }
