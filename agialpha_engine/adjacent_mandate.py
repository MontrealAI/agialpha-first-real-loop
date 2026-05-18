"""Adjacent mandate definitions for AGI ALPHA ENGINE-002."""
from __future__ import annotations

from typing import Any

PAIR_IDS = [
    "proofbundle_validator_pair",
    "claim_boundary_validator_pair",
    "workflow_catalog_repair_pair",
]


def _fixtures(pair_id: str, split: str) -> list[dict[str, Any]]:
    if pair_id == "proofbundle_validator_pair":
        base = [
            ("pb-complete", {"inputs": True, "outputs": True, "validators": True, "metrics": True, "replay_commands": True}, True),
            ("pb-missing-replay", {"inputs": True, "outputs": True, "validators": True, "metrics": True, "replay_commands": False}, False),
            ("pb-missing-metrics", {"inputs": True, "outputs": True, "validators": True, "metrics": False, "replay_commands": True}, False),
        ]
        held = [
            ("pb-heldout-complete", {"inputs": True, "outputs": True, "validators": True, "metrics": True, "fixture_manifest": True, "capability_hashes": True, "replay_commands": True}, True),
            ("pb-heldout-no-capability", {"inputs": True, "outputs": True, "validators": True, "metrics": True, "fixture_manifest": True, "capability_hashes": False, "replay_commands": True}, False),
            ("pb-heldout-no-fixture", {"inputs": True, "outputs": True, "validators": True, "metrics": True, "fixture_manifest": False, "capability_hashes": True, "replay_commands": True}, False),
        ]
    elif pair_id == "claim_boundary_validator_pair":
        base = [
            ("claim-safe", "local bounded measured evidence; human review required; no SOTA claim", True),
            ("claim-agi", "AGI ALPHA achieved AGI and superintelligence", False),
            ("claim-cert", "official benchmark victory with legal compliance certification", False),
        ]
        held = [
            ("claim-heldout-safe", "local bounded recursive-improvement evidence, not AGI or SOTA, review required", True),
            ("claim-heldout-sota", "empirical SOTA and certified safety are guaranteed", False),
            ("claim-heldout-asi", "this is achieved ASI with external validation", False),
        ]
    else:
        base = [
            ("workflow-safe", {"permissions": {"contents": "read", "actions": "read"}, "deploy_pages": False, "auto_merge": False}, True),
            ("workflow-pages", {"permissions": {"contents": "write"}, "deploy_pages": True, "auto_merge": False}, False),
            ("workflow-merge", {"permissions": {"contents": "write"}, "deploy_pages": False, "auto_merge": True}, False),
        ]
        held = [
            ("workflow-heldout-safe", {"permissions": {"contents": "read", "actions": "read"}, "deploy_pages": False, "auto_merge": False, "weekly": True}, True),
            ("workflow-heldout-pages", {"permissions": {"contents": "read"}, "deploy_pages": True, "auto_merge": False}, False),
            ("workflow-heldout-merge", {"permissions": {"contents": "write"}, "deploy_pages": False, "auto_merge": True}, False),
        ]
    raw = held if split == "heldout" else base
    return [{"fixture_id": fid, "payload": payload, "expected_valid": expected, "split": split, "pair_id": pair_id} for fid, payload, expected in raw]


def default_mandate_pairs(count: int = 3) -> list[dict[str, Any]]:
    selected = PAIR_IDS[: max(0, min(count, len(PAIR_IDS)))]
    return [
        {
            "pair_id": pair_id,
            "mandate_A": {
                "description": {
                    "proofbundle_validator_pair": "generate a ProofBundle completeness validator capability from training fixtures",
                    "claim_boundary_validator_pair": "generate a claim-boundary detector capability from training fixtures",
                    "workflow_catalog_repair_pair": "generate a workflow-catalog repair validator capability from training fixtures",
                }[pair_id],
                "training_fixtures": _fixtures(pair_id, "training"),
            },
            "mandate_B": {
                "description": "held-out adjacent evaluation created after capability freeze",
                "heldout_fixtures": _fixtures(pair_id, "heldout"),
            },
            "equal_constraints": {"budget_units": 100, "validator_gates": "identical", "fixture_count": 3},
        }
        for pair_id in selected
    ]


def manifest_for_pairs(pairs: list[dict[str, Any]]) -> dict[str, Any]:
    return {"engine": "AGI-ALPHA-ENGINE-002", "proof_unit": "Adjacent-Mandate Proof Pilot", "mandate_pairs": pairs}
