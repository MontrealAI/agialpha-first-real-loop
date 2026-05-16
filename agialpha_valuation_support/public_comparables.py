from __future__ import annotations

import json
from pathlib import Path

EXPECTED_SCHEMA = "agialpha.valuation_support_public_comparables.v2"


def load_public_comparables(path: Path) -> dict:
    if not Path(path).exists():
        return {"schema_version": EXPECTED_SCHEMA, "comparables": []}

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != EXPECTED_SCHEMA:
        raise ValueError(
            "invalid comparables schema_version: expected "
            f"{EXPECTED_SCHEMA}, got {data.get('schema_version')!r}"
        )
    if not isinstance(data.get("comparables"), list):
        raise ValueError("invalid comparables payload: 'comparables' must be a list")
    return data


def first_comparable(data: dict) -> dict:
    rows = data.get("comparables") or []
    return rows[0] if rows else {}
