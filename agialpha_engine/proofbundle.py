"""ProofBundle creation and replay hash verification helpers.

Supports legacy ENGINE-002 proof artifacts and ENGINE-003 network-skill bundles.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .context import BOUNDARIES, atomic_write_json
from .sandbox import artifact_hash


def make_proofbundle(bundle_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    sections = {
        "inputs_hash": artifact_hash(payload.get("inputs", {})),
        "outputs_hash": artifact_hash(payload.get("outputs", {})),
        "validators_hash": artifact_hash(payload.get("validators", {})),
        "metrics_hash": artifact_hash(payload.get("metrics", {})),
        "fixture_manifest_hash": artifact_hash(payload.get("fixture_manifest", {})),
        "capability_packages_hash": artifact_hash(payload.get("capability_packages", {})),
        "replay_commands_hash": artifact_hash(payload.get("replay_commands", [])),
    }
    bundle = {"schema_version": "agialpha.engine002.proofbundle.v1", "proofbundle_id": bundle_id, **sections, "complete": all(sections.values()), **BOUNDARIES}
    bundle["proofbundle_hash"] = artifact_hash(bundle)
    return bundle


def write_proofbundles(run_dir: Path, payload: dict[str, Any], pair_ids: list[str]) -> dict[str, Any]:
    pdir = run_dir / "10_proofbundles" / "proofbundles"
    bundles = []
    for pair_id in pair_ids:
        bundle = make_proofbundle(f"proofbundle-engine002-{pair_id}", {**payload, "inputs": {"pair_id": pair_id, **payload.get("inputs", {})}})
        atomic_write_json(pdir / f"{pair_id}.json", bundle)
        bundles.append(bundle)
    index = {"schema_version": "agialpha.engine002.proofbundle_index.v1", "proofbundles": bundles, "proofbundle_complete": all(b.get("complete") for b in bundles), **BOUNDARIES}
    atomic_write_json(run_dir / "10_proofbundles" / "proofbundle_index.json", index)
    return index


def verify_proofbundle_hash(bundle: dict[str, Any]) -> bool:
    expected = bundle.get("proofbundle_hash")
    body = {k: v for k, v in bundle.items() if k != "proofbundle_hash"}
    return expected == artifact_hash(body)


def make_network_skill_proofbundle(bundle_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Build deterministic Engine-003 network skill proofbundle payload."""
    keys = [
        "source_job_hash",
        "source_agent_hash",
        "raw_evaluator_log_hashes",
        "validator_result_hashes",
        "skill_package_hash",
        "network_skill_vault_entry_hash",
        "agent_skill_manifest_hashes",
        "skill_import_event_hashes",
        "heldout_test_hashes",
        "b6_vs_b5_comparison_hash",
        "replay_report_hash",
        "falsification_audit_hash",
        "claim_gate_hash",
    ]
    sections = {k: payload.get(k, "") for k in keys}
    bundle = {
        "schema_version": "agialpha.network_skill.proofbundle.v1",
        "proofbundle_id": bundle_id,
        "seed": payload.get("seed"),
        "environment_info": payload.get("environment_info", {}),
        "replay_command": payload.get("replay_command", ""),
        "human_review_status": payload.get("human_review_status", "pending"),
        **sections,
        **BOUNDARIES,
    }
    bundle["complete"] = all(bool(bundle.get(k)) for k in keys)
    bundle["proofbundle_hash"] = artifact_hash({k: v for k, v in bundle.items() if k != "proofbundle_hash"})
    return bundle
