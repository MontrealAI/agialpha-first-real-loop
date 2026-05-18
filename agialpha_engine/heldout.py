"""Held-out fixture management and leakage checks."""
from __future__ import annotations

from typing import Any

from .sandbox import artifact_hash


def heldout_manifest(pairs: list[dict[str, Any]], freeze_hashes: dict[str, str]) -> dict[str, Any]:
    fixtures = []
    for pair in pairs:
        for fixture in pair["mandate_B"]["heldout_fixtures"]:
            rec = dict(fixture)
            rec["created_after_capability_hash"] = freeze_hashes[pair["pair_id"]]
            rec["fixture_hash"] = artifact_hash(rec)
            fixtures.append(rec)
    return {"heldout_generated_after_freeze": True, "heldout_fixtures": fixtures}


def check_leakage(pairs: list[dict[str, Any]]) -> dict[str, Any]:
    training_ids = {f["fixture_id"] for p in pairs for f in p["mandate_A"]["training_fixtures"]}
    heldout_ids = {f["fixture_id"] for p in pairs for f in p["mandate_B"]["heldout_fixtures"]}
    overlap = sorted(training_ids & heldout_ids)
    return {"heldout_leakage_detected": bool(overlap), "overlapping_fixture_ids": overlap}
