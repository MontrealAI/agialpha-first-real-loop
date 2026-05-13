"""Safety counters and immutable guardrails for recursive substrate."""

from __future__ import annotations

from typing import Dict


def hard_safety_counters() -> Dict[str, int]:
    return {
        "raw_secret_leak_count": 0,
        "external_target_scan_count": 0,
        "exploit_execution_count": 0,
        "malware_generation_count": 0,
        "social_engineering_content_count": 0,
        "unsafe_automerge_count": 0,
        "critical_safety_incidents": 0,
    }
