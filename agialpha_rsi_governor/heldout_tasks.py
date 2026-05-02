"""Held-out task generation helpers for RSI-GOVERNOR-001."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def generate_heldout_tasks(repo_root: str | Path, *, lock_hash: str = "", seed: str = "public-fixed-seed") -> list[dict[str, Any]]:
    """Load canonical held-out tasks and stamp deterministic lock metadata."""
    root = Path(repo_root)
    tasks_path = root / "rsi_governor_tasks/heldout/tasks.json"
    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
    digest_input = json.dumps(tasks, sort_keys=True) + f"|{lock_hash}|{seed}"
    lock_digest = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()
    for task in tasks:
        if isinstance(task, dict):
            task.setdefault("lock_hash", lock_hash or "not_reported")
            task.setdefault("generator_seed", seed)
            task.setdefault("generator_digest", lock_digest)
    return tasks
