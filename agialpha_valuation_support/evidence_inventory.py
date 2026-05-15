from __future__ import annotations

from pathlib import Path
from .boundaries import REQUIRED_BOUNDARY_TEXT

ARTIFACT_CHECKS = [
    ("agialpha_ascension_os_package", "agialpha_ascension_os", "core implementation package"),
    ("ascension_os_registry", "ascension_os_registry", "registry evidence"),
    ("ascension_os_runs", "ascension-os-runs", "local replay runs"),
    ("scorecard_runs", "ascension-scorecard-runs", "scorecard runs"),
    ("evidence_registry", "evidence_registry", "evidence dockets"),
    ("secure_rails_checks", "scripts/secure_rails_claim_boundary_check.py", "governance checks"),
    ("workflows", ".github/workflows", "ci workflow support"),
    ("docs", "docs", "operator and reviewer docs"),
    ("tests", "tests", "deterministic tests"),
    ("generated_valuation_data", "docs/_generated/valuation-support", "mission control data"),
]


def build_evidence_inventory(repo_root: Path) -> list[dict]:
    repo_root = Path(repo_root)
    items = []
    for artifact_type, rel_path, relevance in ARTIFACT_CHECKS:
        path = repo_root / rel_path
        exists = path.exists()
        items.append(
            {
                "artifact_type": artifact_type,
                "path": rel_path,
                "exists": exists,
                "validated": True if exists else "not_reported",
                "evidence_level": "local" if exists else "not_reported",
                "valuation_relevance": relevance,
                "claim_boundary": REQUIRED_BOUNDARY_TEXT,
            }
        )
    return items
