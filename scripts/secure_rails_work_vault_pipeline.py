#!/usr/bin/env python3
"""Deterministic SecureRails Work Vault pipeline generator."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

CLAIM_BOUNDARY = (
    "No Evidence Docket, no empirical SOTA claim. "
    "Autonomous evidence production is allowed; autonomous claim promotion is not."
)
SCHEMA_VERSION = "agialpha.securerails.work_vault_record.v1"
DEFAULT_CREATED_AT = "1970-01-01T00:00:00+00:00"
JOB_TYPES = {"defensive_remediation", "defensive_triage", "defensive_validation"}
JOB_STATUSES = {"completed", "rejected", "escalated"}
REVIEW_DECISIONS = {"safe_remediation", "reject", "escalate"}


def canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _short(prefix: str, material: str, length: int = 16) -> str:
    return f"{prefix}-{material[:length]}"


def _require_non_empty_string(payload: Dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _validate_created_at(value: str) -> str:
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("created_at must be an ISO 8601 date-time string") from exc
    if parsed.tzinfo is None:
        raise ValueError("created_at must include timezone offset")
    return value


def validate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    validated = {
        "vault_id": _require_non_empty_string(payload, "vault_id"),
        "defensive_scope": _require_non_empty_string(payload, "defensive_scope"),
        "sovereign_id": _require_non_empty_string(payload, "sovereign_id"),
        "reviewed_by": _require_non_empty_string(payload, "reviewed_by"),
    }

    created_at = payload.get("created_at", DEFAULT_CREATED_AT)
    if not isinstance(created_at, str):
        raise ValueError("created_at must be a string when provided")
    validated["created_at"] = _validate_created_at(created_at)

    mark_units = payload.get("mark_units")
    if isinstance(mark_units, bool) or not isinstance(mark_units, int) or mark_units < 0:
        raise ValueError("mark_units must be an integer >= 0")
    validated["mark_units"] = mark_units

    job_type = payload.get("job_type")
    if job_type not in JOB_TYPES:
        raise ValueError(f"job_type must be one of {sorted(JOB_TYPES)}")
    validated["job_type"] = job_type

    status = payload.get("status")
    if status not in JOB_STATUSES:
        raise ValueError(f"status must be one of {sorted(JOB_STATUSES)}")
    validated["status"] = status

    decision = payload.get("decision")
    if decision not in REVIEW_DECISIONS:
        raise ValueError(f"decision must be one of {sorted(REVIEW_DECISIONS)}")
    validated["decision"] = decision

    reviewers = payload.get("reviewers")
    if not isinstance(reviewers, list) or not reviewers:
        raise ValueError("reviewers must be a non-empty list")
    if not all(isinstance(r, str) and r.strip() for r in reviewers):
        raise ValueError("reviewers entries must be non-empty strings")
    validated["reviewers"] = reviewers

    return validated


def generate_record(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload = validate_payload(payload)
    canonical_input = canonical_json(payload)
    digest = hashlib.sha256(canonical_input.encode("utf-8")).hexdigest()
    mark_hash = hashlib.sha256(f"mark:{digest}".encode("utf-8")).hexdigest()
    job_hash = hashlib.sha256(f"job:{digest}".encode("utf-8")).hexdigest()
    bundle_hash = hashlib.sha256(f"proof:{digest}".encode("utf-8")).hexdigest()
    docket_hash = hashlib.sha256(f"docket:{digest}".encode("utf-8")).hexdigest()

    return {
        "schema_version": SCHEMA_VERSION,
        "work_vault": {
            "vault_id": payload["vault_id"],
            "run_id": _short("svr", digest),
            "created_at": payload["created_at"],
            "defensive_scope": payload["defensive_scope"],
        },
        "mark_allocation": {
            "mark_id": _short("mark", mark_hash, 12),
            "allocation_units": payload["mark_units"],
            "replay_required": True,
            "human_review_required": True,
        },
        "sovereign_assignment": {
            "sovereign_id": payload["sovereign_id"],
            "sovereign_policy": "defensive-remediation-only",
            "reviewers": payload["reviewers"],
        },
        "agi_job": {"job_id": _short("job", job_hash), "job_type": payload["job_type"], "status": payload["status"]},
        "proof_bundle": {
            "proof_bundle_id": _short("pb", bundle_hash, 17),
            "sha256": hashlib.sha256(f"{mark_hash}:{job_hash}:{bundle_hash}:{docket_hash}".encode("utf-8")).hexdigest(),
        },
        "evidence_docket": {"docket_id": _short("dkt", docket_hash), "claim_boundary_statement": CLAIM_BOUNDARY},
        "human_review": {"decision": payload["decision"], "reviewed_by": payload["reviewed_by"]},
        "utility_settlement": {"receipt_id": _short("util", digest, 20), "mode": "$AGIALPHA_UTILITY_ONLY", "real_transfer": False},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    record = generate_record(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
