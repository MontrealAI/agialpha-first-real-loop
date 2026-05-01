"""Conservative repair-plan generation for Evidence Hub registry/site health."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def resolve_registry_path(registry_dir: str = "evidence_registry", repo_root: str = ".") -> Path:
    root = Path(repo_root).resolve()
    reg = Path(registry_dir)
    if not reg.is_absolute():
        reg = (root / reg).resolve()
    return reg


def generate_repair_plan(registry_dir: str = "evidence_registry", repo_root: str = ".") -> Dict[str, Any]:
    """Create a safe, non-destructive repair plan from known index/health files."""
    reg = resolve_registry_path(registry_dir, repo_root)
    idx = reg / "indexes"

    parse_errors: List[str] = []

    def _load(path: Path, default) -> Tuple[Any, bool]:
        if path.exists():
            try:
                return json.loads(path.read_text()), False
            except json.JSONDecodeError:
                parse_errors.append(str(path))
                return default, True
        return default, False

    broken_routes, _ = _load(idx / "broken_routes.json", [])
    shallow_pages, _ = _load(idx / "shallow_pages.json", [])
    low_conf, _ = _load(idx / "low_confidence_discoveries.json", [])

    actions: List[Dict[str, str]] = []
    if broken_routes:
        actions.append({"action": "rebuild_legacy_routes", "reason": "broken_routes_detected"})
    if shallow_pages:
        actions.append({"action": "render_bounded_summaries", "reason": "shallow_pages_detected"})
    if low_conf:
        actions.append({"action": "surface_discoveries", "reason": "low_confidence_needs_manifest"})
    if parse_errors:
        actions.append({"action": "investigate_registry_parse_failure", "reason": "malformed_index_json"})
    if not actions:
        actions.append({"action": "no_op", "reason": "no_defects_detected"})

    return {
        "status": "error" if parse_errors else "success",
        "safe_only": True,
        "auto_merge": False,
        "registry": str(reg),
        "repo_root": str(Path(repo_root)),
        "actions": actions,
        "parse_errors": parse_errors,
    }
