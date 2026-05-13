"""AI-improves-AI orchestration helpers."""

from __future__ import annotations

from typing import Dict, Any


def candidate_lock_manifest(locked: bool = True) -> Dict[str, Any]:
    return {
        "locked": locked,
        "rule": "held-out fixtures must be generated after lock",
        "autonomous_persistence": False,
        "human_review_required": True,
    }
