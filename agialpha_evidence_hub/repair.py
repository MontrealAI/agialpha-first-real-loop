"""Conservative repair-plan generation for Evidence Hub registry/site health."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def generate_repair_plan(registry_dir: str = "evidence_registry", repo_root: str = ".") -> Dict[str, Any]:
    """Create a safe, non-destructive repair plan from known index/health files."""
    reg = Path(registry_dir)
    idx = reg / "indexes"

    def _load(path: Path, default):
        if path.exists():
            try:
                return json.loads(path.read_text())
            except json.JSONDecodeError:
                return default
        return default

    broken_routes = _load(idx / "broken_routes.json", [])
    shallow_pages = _load(idx / "shallow_pages.json", [])
    low_conf = _load(idx / "low_confidence_discoveries.json", [])

    actions: List[Dict[str, str]] = []
    if broken_routes:
        actions.append({"action": "rebuild_legacy_routes", "reason": "broken_routes_detected"})
    if shallow_pages:
        actions.append({"action": "render_bounded_summaries", "reason": "shallow_pages_detected"})
    if low_conf:
        actions.append({"action": "surface_discoveries", "reason": "low_confidence_needs_manifest"})
    if not actions:
        actions.append({"action": "no_op", "reason": "no_defects_detected"})

    return {
        "status": "success",
        "safe_only": True,
        "auto_merge": False,
        "registry": str(reg),
        "repo_root": str(Path(repo_root)),
        "actions": actions,
    }
