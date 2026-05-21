"""Baseline evaluator for measured recursive machine-labor runs."""
from __future__ import annotations

from typing import Any


def _safe_rate(num: float, den: float) -> float:
    return 0.0 if den <= 0 else round(num / den, 6)


def evaluate_baseline(results: list[dict[str, Any]], *, use_archive: bool) -> dict[str, Any]:
    total = len(results)
    accepted = [r for r in results if r.get("accepted") is True]
    replayed = [r for r in accepted if r.get("replay_pass") is True]
    validated = [r for r in accepted if r.get("validator_pass") is True]
    verified_work_score = round(sum(float(r.get("score", 0.0)) for r in accepted), 6)
    return {
        "task_count": total,
        "accepted_task_count": len(accepted),
        "accepted_task_rate": _safe_rate(len(accepted), total),
        "validator_pass_rate": _safe_rate(len(validated), len(accepted) or 1),
        "replay_pass_rate": _safe_rate(len(replayed), len(accepted) or 1),
        "verified_work_score": verified_work_score,
        "archive_used": bool(use_archive),
    }


def evaluate_all_baselines(raw: dict[str, Any]) -> dict[str, Any]:
    b5 = evaluate_baseline(raw.get("b5_results", []), use_archive=False)
    b6 = evaluate_baseline(raw.get("b6_results", []), use_archive=True)
    return {
        "B5_no_archive": b5,
        "B6_archive_reuse": b6,
    }
