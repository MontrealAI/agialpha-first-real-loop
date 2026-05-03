#!/usr/bin/env python3
"""SecureRails no-auto-merge check.

Scans all GitHub Actions workflow files in the repository to ensure none of
them use the `auto-merge` or `merge` GitHub CLI/API calls that would enable
autonomous merging without human approval.

Usage:
    python scripts/secure_rails_no_automerge_check.py <repo_root>

Exits 0 if no violations are found, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Patterns that indicate an attempt to auto-merge without human gating
AUTOMERGE_PATTERNS: list[tuple[str, str]] = [
    (r"gh\s+pr\s+merge\b", "gh pr merge call (auto-merge risk)"),
    (r"--auto\b", "--auto flag (enables GitHub auto-merge)"),
    (r"enable[-_]auto[-_]merge", "enable_auto_merge API call"),
    (r"auto[-_]merge\s*:\s*true", "auto_merge: true in workflow config"),
    (r"merge_method\s*:", "merge_method without human gate"),
]


def _scan_workflows(repo_root: Path) -> list[str]:
    wf_dir = repo_root / ".github" / "workflows"
    if not wf_dir.is_dir():
        return []

    violations: list[str] = []
    for wf_path in sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml")):
        try:
            text = wf_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern, label in AUTOMERGE_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                line_no = text[: match.start()].count("\n") + 1
                violations.append(
                    f"{wf_path.name}:{line_no}: {label} — matched: {match.group()!r}"
                )
    return violations


def main() -> int:
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    repo_root = repo_root.resolve()

    print(f"[SecureRails] No-auto-merge check: scanning {repo_root / '.github' / 'workflows'}")
    violations = _scan_workflows(repo_root)

    if violations:
        print("[SecureRails] FAIL — auto-merge posture detected:")
        for v in violations:
            print(f"  {v}")
        return 1

    print("[SecureRails] PASS — no auto-merge posture detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
