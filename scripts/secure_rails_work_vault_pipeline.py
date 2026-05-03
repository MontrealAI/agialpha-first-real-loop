#!/usr/bin/env python3
"""Deterministic SecureRails Work Vault record generator."""
import argparse
import hashlib
import json
from datetime import datetime

CLAIM_BOUNDARY = "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."

ALLOWED_JOB_TYPES = {"defensive_remediation", "defensive_triage", "defensive_validation"}
ALLOWED_JOB_STATUS = {"completed", "rejected", "escalated"}
ALLOWED_DECISIONS = {"safe_remediation", "reject", "escalate"}


def _stable_hash(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_created_at(value: str) -> None:
    if not isinstance(value, str):
        raise ValueError("created_at must be a string in RFC3339 date-time format")
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"Invalid created_at date-time: {value}") from exc
    if parsed.tzinfo is None:
        raise ValueError("created_at must include timezone offset (RFC3339)")


def _validate_payload(payload: dict) -> None:
    if payload["job_type"] not in ALLOWED_JOB_TYPES:
        raise ValueError(f"Invalid job_type: {payload['job_type']}")
    if payload["status"] not in ALLOWED_JOB_STATUS:
        raise ValueError(f"Invalid status: {payload['status']}")
    if payload["decision"] not in ALLOWED_DECISIONS:
        raise ValueError(f"Invalid decision: {payload['decision']}")
    mark_units = payload["mark_units"]
    if isinstance(mark_units, bool) or not isinstance(mark_units, int):
        raise ValueError("mark_units must be an integer (boolean is not allowed)")
    if mark_units < 0:
        raise ValueError(f"mark_units must be non-negative: {mark_units}")
    _validate_created_at(payload.get("created_at", "1970-01-01T00:00:00+00:00"))

    reviewers = payload["reviewers"]
    if not isinstance(reviewers, list) or len(reviewers) < 1:
        raise ValueError("reviewers must be a non-empty list of strings")
    if any(not isinstance(r, str) or not r for r in reviewers):
        raise ValueError("reviewers entries must be non-empty strings")


def build_record(payload: dict) -> dict:
    _validate_payload(payload)
    digest = _stable_hash(payload)
    run_id = f"svr-{digest[:16]}"
    job_id = f"job-{digest[16:32]}"
    proof_id = f"pb-{digest[32:48]}"
    docket_id = f"dkt-{digest[48:64]}"
    record = {
        "schema_version": "agialpha.securerails.work_vault_record.v1",
        "work_vault": {
            "vault_id": payload["vault_id"],
            "run_id": run_id,
            "created_at": payload.get("created_at", "1970-01-01T00:00:00+00:00"),
            "defensive_scope": payload["defensive_scope"],
        },
        "mark_allocation": {
            "mark_id": f"mark-{digest[:12]}",
            "allocation_units": payload["mark_units"],
            "replay_required": True,
            "human_review_required": True,
        },
        "sovereign_assignment": {
            "sovereign_id": payload["sovereign_id"],
            "sovereign_policy": "defensive-remediation-only",
            "reviewers": payload["reviewers"],
        },
        "agi_job": {"job_id": job_id, "job_type": payload["job_type"], "status": payload["status"]},
        "proof_bundle": {"proof_bundle_id": proof_id, "sha256": digest},
        "evidence_docket": {"docket_id": docket_id, "claim_boundary_statement": CLAIM_BOUNDARY},
        "human_review": {"decision": payload["decision"], "reviewed_by": payload["reviewed_by"]},
        "utility_settlement": {"receipt_id": f"util-{digest[:20]}", "mode": "$AGIALPHA_UTILITY_ONLY", "real_transfer": False},
    }
    return record


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)
    record = build_record(payload)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, sort_keys=True)
        f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
