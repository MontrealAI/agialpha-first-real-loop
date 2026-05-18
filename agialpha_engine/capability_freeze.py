"""Capability freeze records and mutation checks."""
from __future__ import annotations

from typing import Any

from .sandbox import artifact_hash


def freeze_capability(pair: dict[str, Any], training_results: list[dict[str, Any]]) -> dict[str, Any]:
    rules = {
        "proofbundle_validator_pair": ["require_inputs", "require_outputs", "require_validators", "require_metrics", "require_fixture_manifest", "require_capability_hashes", "require_replay_commands"],
        "claim_boundary_validator_pair": ["block_agi_asi_superintelligence", "block_sota_certification", "block_external_validation_overclaim", "require_local_bounded_human_review"],
        "workflow_catalog_repair_pair": ["require_read_only_permissions", "block_pages_deploy", "block_auto_merge"],
    }[pair["pair_id"]]
    package = {
        "capability_id": f"capability-{pair['pair_id']}",
        "pair_id": pair["pair_id"],
        "generated_from": [r["fixture_id"] for r in training_results],
        "accepted_training_score": sum(1 for r in training_results if r["correct"]),
        "rules": rules,
        "frozen": True,
        "post_freeze_edit_allowed": False,
    }
    package["capability_hash"] = artifact_hash(package)
    return package


def verify_frozen(capability: dict[str, Any]) -> dict[str, Any]:
    expected = capability.get("capability_hash")
    body = {k: v for k, v in capability.items() if k != "capability_hash"}
    actual = artifact_hash(body)
    return {"capability_id": capability.get("capability_id"), "expected_hash": expected, "actual_hash": actual, "mutation_detected": expected != actual, "capability_freeze_valid": expected == actual and capability.get("frozen") is True}


def mutate_for_test(capability: dict[str, Any]) -> dict[str, Any]:
    changed = dict(capability)
    changed["rules"] = list(changed.get("rules", [])) + ["post_freeze_mutation"]
    return changed
