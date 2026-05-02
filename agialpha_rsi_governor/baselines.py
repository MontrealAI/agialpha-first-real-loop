"""Baseline ladder helpers for RSI-GOVERNOR-001."""

from __future__ import annotations


def compute_baseline_ladder(b5_score: float, b6_score: float) -> dict:
    """Return explicit B0..B7 representation with B5/B6 scores."""
    return {
        "B0": {"name": "no governance kernel", "score": "not_reported"},
        "B1": {"name": "static checklist governance", "score": "not_reported"},
        "B2": {"name": "current simple publisher", "score": "not_reported"},
        "B3": {"name": "heuristic hub repair", "score": "not_reported"},
        "B4": {"name": "unstructured self-modification", "score": "not_reported"},
        "B5": {"name": "incumbent kernel", "score": b5_score},
        "B6": {"name": "candidate kernel", "score": b6_score},
        "B7": {"name": "human-governed promoted kernel", "score": "pending"},
    }


__all__ = ["compute_baseline_ladder"]
