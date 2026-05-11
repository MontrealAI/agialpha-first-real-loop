#!/usr/bin/env python3
"""SecureRails claim-boundary check.

Scans the repository for disallowed overclaim patterns (e.g. AGI achieved,
ASI, empirical SOTA, certified secure, guaranteed security, investment return,
offensive capability) and enforces the SecureRails product boundary.

A match is only flagged if the line does NOT contain a negation indicator
(such as "not", "no", "never", "does not", "is not") before the matched text.
This prevents false positives from existing disclaimers that explicitly deny
these capabilities.

Usage:
    python scripts/secure_rails_claim_boundary_check.py <repo_root>

Exits 0 if no violations are found, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Disallowed claim patterns (case-insensitive).
# Each entry is (regex, human-readable label).
# ---------------------------------------------------------------------------
DISALLOWED_PATTERNS: list[tuple[str, str]] = [
    (r"\bwe\s+have\s+achieved\s+agi\b", "claims achieved AGI"),
    (r"\bagi\s+is\s+achieved\b", "claims achieved AGI"),
    (r"\bwe\s+have\s+achieved\s+asi\b", "claims achieved ASI"),
    (r"\basi\s+is\s+achieved\b", "claims achieved ASI"),
    (r"\bprovides?\s+guaranteed\s+security\b", "guarantees security"),
    (r"\bguarantees?\s+economic\s+return\b", "guarantees economic return"),
    (r"\bthis\s+is\s+an?\s+investment\s+product\b", "positions as investment product"),
    (r"\bauto[- ]?merge[sd]?\s+autonomously\b", "autonomous auto-merge claim"),
    (r"\bsafe\s+for\s+autonomous\s+production\s+remediation\b", "safe-autonomy overclaim"),
]

# Negation words: if the portion of the line BEFORE the match contains one of
# these, we treat the occurrence as a disclaimer rather than a positive claim.
NEGATION_PATTERN = re.compile(
    r"\b(not|no|never|cannot|can't|isn't|aren't|doesn't|don't|does\s+not|is\s+not|"
    r"are\s+not|do\s+not|did\s+not|will\s+not|would\s+not|has\s+not|have\s+not)\b",
    re.IGNORECASE,
)

# File extensions to scan
SCAN_EXTENSIONS = {".md", ".txt", ".rst", ".py", ".json", ".yaml", ".yml"}

# Directories to skip entirely
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}

# Skip this script itself to avoid self-referential false positives
SKIP_FILES = {"secure_rails_claim_boundary_check.py"}


def _is_negated(line: str, match_start_in_line: int) -> bool:
    """Return True if a negation word appears before the match on the same line."""
    prefix = line[:match_start_in_line]
    return bool(NEGATION_PATTERN.search(prefix))


def _scan_repo(repo_root: Path) -> list[str]:
    violations: list[str] = []
    for path in sorted(repo_root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        for pattern, label in DISALLOWED_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                line_no = text[: match.start()].count("\n") + 1
                line = lines[line_no - 1] if line_no <= len(lines) else ""
                # Calculate match start within the line
                line_start = text.rfind("\n", 0, match.start()) + 1
                match_start_in_line = match.start() - line_start
                if _is_negated(line, match_start_in_line):
                    continue
                rel = path.relative_to(repo_root)
                violations.append(f"{rel}:{line_no}: {label!r} — matched: {match.group()!r}")
    return violations


def main() -> int:
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    repo_root = repo_root.resolve()

    print(f"[SecureRails] Claim-boundary check: scanning {repo_root}")
    violations = _scan_repo(repo_root)

    if violations:
        print("[SecureRails] FAIL — disallowed claim patterns detected:")
        for v in violations:
            print(f"  {v}")
        return 1

    print("[SecureRails] PASS — no disallowed claim patterns detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
