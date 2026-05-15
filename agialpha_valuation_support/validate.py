from __future__ import annotations

from pathlib import Path

FORBIDDEN_PHRASES = [
    "agi alpha is worth",
    "fair market value",
    "guaranteed valuation",
    "guaranteed return",
    "token appreciation",
    "buy",
    "sell",
    "hold",
    "profit rights",
    "ownership rights",
    "achieved agi",
    "achieved asi",
    "achieved superintelligence",
    "empirical sota",
    "certified",
    "eu ai act exempt",
    "legally approved worldwide",
    "recursive beaten",
]


def scan_forbidden_language(run_dir: Path) -> list[str]:
    violations: list[str] = []
    run_dir = Path(run_dir)
    for path in sorted(run_dir.iterdir()):
        if path.suffix not in {".json", ".md"}:
            continue
        text = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                violations.append(f"{path.name}: {phrase}")
    return violations
