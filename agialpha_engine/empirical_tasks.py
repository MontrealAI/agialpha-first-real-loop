"""Empirical task loading helpers for Engine-002 fixtures."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_task_manifest(task_dir: Path) -> dict[str, Any]:
    task_dir = Path(task_dir)
    task = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))
    fixture = json.loads((task_dir / "fixture.json").read_text(encoding="utf-8"))
    return {
        "task_id": task.get("task_id", task_dir.name),
        "task_dir": str(task_dir),
        "task": task,
        "fixture": fixture,
        "expected": task.get("expected", {}),
    }


def discover_tasks(root: Path) -> list[dict[str, Any]]:
    root = Path(root)
    manifests: list[dict[str, Any]] = []
    for task_file in sorted(root.glob("**/task.json")):
        manifests.append(load_task_manifest(task_file.parent))
    return manifests
