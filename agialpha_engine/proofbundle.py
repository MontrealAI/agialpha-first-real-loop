"""ProofBundle creation and replay hash verification for Engine-002."""
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
