#!/usr/bin/env python3
"""SecureRails EU AI Act use-case triage check.

Validates a deployment-intake JSON file against the SecureRails product
boundary and the EU AI Act Annex III exclusions.

Rules enforced:
  - use_case must be present and describe defensive / governance software.
  - hr_worker_evaluation must be false.
  - profiling_natural_persons must be false.
  - automated_decisions_natural_persons must be false.
  - critical_infrastructure_safety_component must be false.
  - gpai_model_provider_claim must be false.
  - offensive_cyber must be false.
  - risk_level, when present, must be "low" or "minimal".

Usage:
    python scripts/secure_rails_use_case_triage_check.py <deployment-intake.json>

Exits 0 if all checks pass, 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Boolean fields that must be explicitly False (i.e. excluded use-cases)
EXCLUDED_FLAGS: list[tuple[str, str]] = [
    ("hr_worker_evaluation", "HR / worker-evaluation use case excluded by SecureRails boundary"),
    ("profiling_natural_persons", "profiling of natural persons excluded by SecureRails boundary"),
    (
        "automated_decisions_natural_persons",
        "automated decision-making about natural persons excluded by SecureRails boundary",
    ),
    (
        "critical_infrastructure_safety_component",
        "critical-infrastructure safety-component reliance excluded by SecureRails boundary",
    ),
    ("gpai_model_provider_claim", "GPAI model-provider claim excluded by SecureRails boundary"),
    ("offensive_cyber", "offensive cyber use excluded by SecureRails boundary"),
]

ALLOWED_RISK_LEVELS = {"low", "minimal"}


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "[SecureRails] USAGE: secure_rails_use_case_triage_check.py <deployment-intake.json>",
            file=sys.stderr,
        )
        return 1

    intake_path = Path(sys.argv[1])
    if not intake_path.exists():
        print(f"[SecureRails] FAIL — intake file not found: {intake_path}", file=sys.stderr)
        return 1

    try:
        intake = json.loads(intake_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[SecureRails] FAIL — invalid JSON in {intake_path}: {exc}", file=sys.stderr)
        return 1

    print(f"[SecureRails] Use-case triage check: {intake_path}")
    failures: list[str] = []

    # use_case must be present and non-empty
    if not intake.get("use_case"):
        failures.append("  'use_case' field is missing or empty")

    # All excluded-use-case flags must be present and False
    for flag, label in EXCLUDED_FLAGS:
        if flag not in intake:
            failures.append(f"  missing required field {flag!r}")
        elif intake[flag] is not False:
            failures.append(f"  {flag!r} must be false — {label}")

    # risk_level, if present, must be low/minimal
    risk = intake.get("risk_level", "").lower()
    if risk and risk not in ALLOWED_RISK_LEVELS:
        failures.append(
            f"  risk_level {intake['risk_level']!r} is not allowed; must be one of {sorted(ALLOWED_RISK_LEVELS)}"
        )

    if failures:
        print("[SecureRails] FAIL — use-case triage violations:")
        for f in failures:
            print(f)
        return 1

    print("[SecureRails] PASS — deployment intake passed use-case triage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
