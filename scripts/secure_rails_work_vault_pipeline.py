#!/usr/bin/env python3
"""Deterministic SecureRails Work Vault pipeline generator."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict

CLAIM_BOUNDARY = (
    "No Evidence Docket, no empirical SOTA claim. "
    "Autonomous evidence production is allowed; autonomous claim promotion is not."
)
SCHEMA_VERSION = "agialpha.securerails.work_vault_record.v1"


def canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _short(prefix: str, material: str, length: int = 16) -> str:
    return f"{prefix}-{material[:length]}"


def generate_record(payload: Dict[str, Any]) -> Dict[str, Any]:
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
        "agi_job": {
            "job_id": _short("job", job_hash),
            "job_type": payload["job_type"],
            "status": payload["status"],
        },
        "proof_bundle": {
            "proof_bundle_id": _short("pb", bundle_hash, 17),
            "sha256": hashlib.sha256(
                f"{mark_hash}:{job_hash}:{bundle_hash}:{docket_hash}".encode("utf-8")
            ).hexdigest(),
        },
        "evidence_docket": {
            "docket_id": _short("dkt", docket_hash),
            "claim_boundary_statement": CLAIM_BOUNDARY,
        },
        "human_review": {
            "decision": payload["decision"],
            "reviewed_by": payload["reviewed_by"],
        },
        "utility_settlement": {
            "receipt_id": _short("util", digest, 20),
            "mode": "$AGIALPHA_UTILITY_ONLY",
            "real_transfer": False,
        },
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
