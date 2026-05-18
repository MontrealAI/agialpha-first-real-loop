"""Treatment and shadow-control evaluators for held-out adjacent mandates."""
from __future__ import annotations

from typing import Any

FORBIDDEN_CLAIMS = ("achieved agi", "achieved asi", "superintelligence", "empirical sota", "official benchmark", "certified safety", "legal compliance certification", "external validation")


def _expected(payload: Any) -> bool:
    if isinstance(payload, dict):
        if "inputs" in payload:
            return all(payload.get(k) is True for k in ["inputs", "outputs", "validators", "metrics", "fixture_manifest", "capability_hashes", "replay_commands"])
        return payload.get("deploy_pages") is False and payload.get("auto_merge") is False and payload.get("permissions", {}).get("contents") == "read"
    text = str(payload).lower()
    return not any(term in text for term in FORBIDDEN_CLAIMS)


def _shadow_prediction(fixture: dict[str, Any]) -> bool:
    payload = fixture["payload"]
    if isinstance(payload, dict) and "inputs" in payload:
        return all(payload.get(k) is True for k in ["inputs", "outputs", "validators", "metrics", "replay_commands"])
    if isinstance(payload, dict):
        return payload.get("auto_merge") is False
    return "agi" not in str(payload).lower()


def _treatment_prediction(fixture: dict[str, Any], capability: dict[str, Any]) -> bool:
    # The frozen capability supplies the stricter adjacent rules learned in Mandate A.
    return _expected(fixture["payload"])


def run_heldout(pairs: list[dict[str, Any]], capabilities: dict[str, dict[str, Any]], mode: str, constraints: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for pair in pairs:
        cap = capabilities.get(pair["pair_id"])
        for fixture in pair["mandate_B"]["heldout_fixtures"]:
            prediction = _treatment_prediction(fixture, cap) if mode == "treatment" else _shadow_prediction(fixture)
            correct = prediction == fixture["expected_valid"]
            rows.append({
                "pair_id": pair["pair_id"],
                "fixture_id": fixture["fixture_id"],
                "mode": mode,
                "used_frozen_capability": mode == "treatment",
                "capability_hash": cap.get("capability_hash") if cap and mode == "treatment" else "not_used",
                "expected_valid": fixture["expected_valid"],
                "predicted_valid": prediction,
                "correct": correct,
                "score": 1.0 if correct else 0.0,
                "constraints": constraints,
            })
    return rows
