#!/usr/bin/env python3
"""SecureRails safety-ledger check.

Validates that a safety-ledger JSON file contains the required hard-counter
fields and that every counter is explicitly 0.

Usage:
    python scripts/secure_rails_safety_ledger_check.py <ledger.json>

Exits 0 if all counters are present and zero, 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_COUNTERS = [
    "raw_secret_leak_count",
    "external_target_scan_count",
    "exploit_execution_count",
    "malware_generation_count",
    "social_engineering_content_count",
    "unsafe_automerge_count",
    "critical_safety_incidents",
]


def main() -> int:
    if len(sys.argv) < 2:
        print("[SecureRails] USAGE: secure_rails_safety_ledger_check.py <ledger.json>", file=sys.stderr)
        return 1

    ledger_path = Path(sys.argv[1])
    if not ledger_path.exists():
        print(f"[SecureRails] FAIL — ledger file not found: {ledger_path}", file=sys.stderr)
        return 1

    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[SecureRails] FAIL — invalid JSON in {ledger_path}: {exc}", file=sys.stderr)
        return 1

    print(f"[SecureRails] Safety-ledger check: {ledger_path}")
    failures: list[str] = []

    for counter in REQUIRED_COUNTERS:
        if counter not in ledger:
            failures.append(f"  missing required counter: {counter!r}")
        elif ledger[counter] != 0:
            failures.append(
                f"  counter {counter!r} must be 0, got {ledger[counter]!r}"
            )

    if failures:
        print("[SecureRails] FAIL — safety-ledger violations:")
        for f in failures:
            print(f)
        return 1

    print("[SecureRails] PASS — all safety counters present and zero.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
