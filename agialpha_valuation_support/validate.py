from __future__ import annotations

from pathlib import Path
import re

FORBIDDEN_PATTERNS = [
    r"agi alpha is worth",
    r"fair market value",
    r"guaranteed valuation",
    r"guaranteed return",
    r"guaranteed roi",
    r"token appreciation",
    r"\bbuy\w*\b",
    r"\bsell\w*\b",
    r"\bhold\w*\b",
    r"securities offering",
    r"profit rights",
    r"ownership rights",
    r"achieved agi",
    r"achieved asi",
    r"achieved superintelligence",
    r"empirical sota",
    r"\bcertified\b",
    r"eu ai act exempt",
    r"legally approved worldwide",
    r"recursive beaten",
]

ALLOWLIST_SNIPPETS = [
    "it is not investment advice, financial advice, a securities offering, a token-value claim",
    "it is not investment advice, financial advice, a securities offering",
]


def scan_forbidden_language(run_dir: Path) -> list[str]:
    violations: list[str] = []
    run_dir = Path(run_dir)
    for path in sorted(run_dir.iterdir()):
        if path.suffix not in {".json", ".md"}:
            continue
        text = path.read_text(encoding="utf-8").lower()
        masked = text
        for snippet in ALLOWLIST_SNIPPETS:
            masked = masked.replace(snippet, "")
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, masked):
                violations.append(f"{path.name}: {pattern}")
    return violations
