from __future__ import annotations

import json
from pathlib import Path

EXPECTED_SCHEMA = "agialpha.valuation_support_public_comparables.v2"


def load_public_comparables(path: Path) -> dict:
    if not Path(path).exists():
        return {"schema_version": EXPECTED_SCHEMA, "comparables": []}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != EXPECTED_SCHEMA:
        data["schema_version"] = EXPECTED_SCHEMA
    if not isinstance(data.get("comparables"), list):
        data["comparables"] = []
    return data


def first_comparable(data: dict) -> dict:
    rows = data.get("comparables") or []
    return rows[0] if rows else {}
