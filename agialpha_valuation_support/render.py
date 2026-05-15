from __future__ import annotations

import json
from pathlib import Path

from .boundaries import REQUIRED_BOUNDARY_TEXT


def render_summary(run_dir: Path) -> str:
    run_dir = Path(run_dir)
    score = json.loads((run_dir / "05_implementation_equivalence_score.json").read_text(encoding="utf-8"))
    missing = json.loads((run_dir / "10_missing_evidence.json").read_text(encoding="utf-8"))
    tier = score.get("readiness_tier", "not_reported")
    eq = score.get("implementation_equivalence_score", "not_reported")
    missing_items = missing.get("missing_evidence", [])
    lines = [
        "# AGI ALPHA Valuation Support Memo",
        "",
        REQUIRED_BOUNDARY_TEXT,
        "",
        "Any comparison to private self-improving-AI labs is limited to public implementation-side evidence available in this repository and manually entered public comparables. Missing external data is shown as not_reported.",
        "",
        f"- Implementation equivalence score: `{eq}`",
        f"- Readiness tier: `{tier}`",
        "- Missing-evidence honesty:",
    ]
    for item in missing_items:
        lines.append(f"  - {item}")
    return "\n".join(lines) + "\n"
