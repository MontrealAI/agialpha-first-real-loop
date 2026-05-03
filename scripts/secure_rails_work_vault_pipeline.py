#!/usr/bin/env python3
"""Deterministic SecureRails Work Vault record generator."""
import argparse
import hashlib
import json

CLAIM_BOUNDARY = "No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not."


def _stable_hash(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_record(payload: dict) -> dict:
    seed = {
        "vault_id": payload["vault_id"],
        "defensive_scope": payload["defensive_scope"],
        "job_type": payload["job_type"],
        "mark_units": payload["mark_units"],
        "sovereign_id": payload["sovereign_id"],
    }
    digest = _stable_hash(seed)
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
