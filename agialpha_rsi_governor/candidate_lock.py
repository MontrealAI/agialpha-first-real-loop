"""Candidate lock helpers for RSI-GOVERNOR-001."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable


def build_candidate_lock_manifest(candidate_dirs: Iterable[Path]) -> dict:
    """Build deterministic lock manifest for candidate kernel directories."""
    entries = []
    for cdir in sorted((Path(p) for p in candidate_dirs), key=lambda p: p.name):
        policy = cdir / "candidate_kernel.json"
        patch = cdir / "candidate.patch"
        policy_bytes = policy.read_bytes() if policy.exists() else b""
        patch_bytes = patch.read_bytes() if patch.exists() else b""
        entries.append(
            {
                "candidate_id": cdir.name,
                "policy_sha256": hashlib.sha256(policy_bytes).hexdigest(),
                "patch_sha256": hashlib.sha256(patch_bytes).hexdigest(),
            }
        )
    root = hashlib.sha256(json.dumps(entries, sort_keys=True).encode("utf-8")).hexdigest()
    return {"candidates": entries, "lock_hash": root}


__all__ = ["build_candidate_lock_manifest"]
