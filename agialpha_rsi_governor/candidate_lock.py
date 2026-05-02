"""Candidate lock helpers for RSI-GOVERNOR-001."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable, List


def _stable_json_bytes(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def candidate_hash(candidate: Dict[str, Any]) -> str:
    """Return deterministic hash for a candidate payload."""
    return hashlib.sha256(_stable_json_bytes(candidate)).hexdigest()


def build_candidate_lock_manifest(candidates: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Lock candidate set before held-out reveal."""
    entries: List[Dict[str, str]] = []
    for c in candidates:
        cid = str(c.get("candidate_id", "unknown"))
        entries.append({"candidate_id": cid, "candidate_hash": candidate_hash(c)})
    entries.sort(key=lambda x: x["candidate_id"])
    root = hashlib.sha256(_stable_json_bytes({"candidates": entries})).hexdigest()
    return {
        "lock_protocol": "lock-before-heldout.v1",
        "candidate_count": len(entries),
        "candidates": entries,
        "lock_hash": root,
    }


__all__ = ["candidate_hash", "build_candidate_lock_manifest"]
