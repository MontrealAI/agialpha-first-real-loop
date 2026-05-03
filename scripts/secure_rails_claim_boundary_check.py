#!/usr/bin/env python3
"""Checks SecureRails docs for core guardrail statements."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

CHECKS = {
    "claim-boundary": "claim boundary",
    "safety-ledger": "safety ledger",
    "no-auto-merge": "no auto-merge",
    "default-use-case-triage": "default use-case triage",
}


def scan_text(root: Path) -> str:
    docs_dir = root / "docs" / "secure-rails"
    if not docs_dir.exists():
        return ""
    parts: list[str] = []
    for p in sorted(docs_dir.rglob("*.md")):
        parts.append(p.read_text(encoding="utf-8", errors="ignore").lower())
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--check", default="claim-boundary", choices=sorted(CHECKS))
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    haystack = scan_text(root)
    needle = CHECKS[args.check]

    if needle not in haystack:
        print(f"missing required phrase for {args.check!r}: {needle!r}", file=sys.stderr)
        return 1

    print(f"ok: found {needle!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
