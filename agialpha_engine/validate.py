"""Validation gates for AGI ALPHA ENGINE-002 proof runs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .metrics import SAFETY_COUNTERS, stronger_claim_supported

REQUIRED_RUN_FILES = [
    "00_manifest.json", "01_claim_boundary.md", "02_mandate_pairs/mandate_pairs.json",
    "03_mandate_A_training/tasks.json", "03_mandate_A_training/raw_results.json", "03_mandate_A_training/generated_capabilities.json",
    "04_capability_freeze/frozen_capabilities.json", "04_capability_freeze/capability_hashes.json", "04_capability_freeze/mutation_check.json",
    "05_heldout_mandate_B/heldout_fixtures.json", "05_heldout_mandate_B/leakage_check.json",
    "06_treatment_run/raw_results.json", "06_treatment_run/validator_results.json",
    "07_shadow_control_run/raw_results.json", "07_shadow_control_run/validator_results.json",
    "08_comparison/computed_metrics.json", "08_comparison/vRCI.json", "08_comparison/B6_vs_B5.json", "08_comparison/treatment_vs_control.md",
    "09_semantic_negative_tests/forbidden_claim_injection.json", "09_semantic_negative_tests/regulated_domain_injection.json",
    "09_semantic_negative_tests/human_review_gate_failure.json", "09_semantic_negative_tests/replay_tampering.json",
    "09_semantic_negative_tests/artifact_hash_mismatch.json", "09_semantic_negative_tests/auto_merge_attempt.json",
    "09_semantic_negative_tests/secret_like_fixture_redaction.json",
    "10_proofbundles/proofbundle_index.json", "11_evidence_dockets/docket_index.json",
    "12_adversarial_docket/failed_runs.json", "12_adversarial_docket/rejected_claims.json",
    "12_adversarial_docket/evaluator_disagreements.json", "12_adversarial_docket/baseline_regressions.json",
    "12_adversarial_docket/falsification_attempts.json", "13_replay/replay_report.json", "14_falsification/falsification_audit.json",
    "15_public_summary/summary.json", "15_public_summary/stronger_claim_status.md", "evidence-run-manifest.json",
]

FORBIDDEN_TEXT = ["achieved AGI", "achieved ASI", "superintelligence", "empirical SOTA", "official benchmark victory", "security certification", "legal compliance certification", "EU AI Act exemption", "token value", "investment return", "ROI", "yield"]
SEMANTIC_NEGATIVE_TEST_FILES = [
    "forbidden_claim_injection",
    "regulated_domain_injection",
    "human_review_gate_failure",
    "replay_tampering",
    "artifact_hash_mismatch",
    "auto_merge_attempt",
    "secret_like_fixture_redaction",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _semantic_negative_tests_validation(run_dir: Path) -> tuple[bool, list[str]]:
    failures: list[str] = []
    for name in SEMANTIC_NEGATIVE_TEST_FILES:
        payload = read_json(run_dir / "09_semantic_negative_tests" / f"{name}.json")
        if payload.get("pass") is not True or payload.get("blocked") is not True:
            failures.append(name)
    return not failures, failures


def validate_run(run_dir: Path) -> dict[str, Any]:
    missing = [p for p in REQUIRED_RUN_FILES if not (run_dir / p).exists()]
    metrics = read_json(run_dir / "08_comparison" / "computed_metrics.json") if not missing else {}
    replay_report = read_json(run_dir / "13_replay" / "replay_report.json") if not missing else {}
    status_text = (run_dir / "15_public_summary" / "stronger_claim_status.md").read_text(encoding="utf-8") if (run_dir / "15_public_summary" / "stronger_claim_status.md").exists() else ""
    forbidden_hits = [term for term in FORBIDDEN_TEXT if term in status_text]
    safety_nonzero = {k: metrics.get(k) for k in SAFETY_COUNTERS if metrics.get(k) not in (0, None)}
    support_consistent = ("supports the local bounded claim" in status_text) == stronger_claim_supported(metrics) if status_text else False
    semantic_negative_tests_pass, failed_semantic_negative_tests = _semantic_negative_tests_validation(run_dir) if not missing else (False, [])
    result = {
        "schema_validation_pass": not missing,
        "missing_required_files": missing,
        "metric_validation_pass": bool(metrics.get("metrics_computed_from_raw_results")),
        "semantic_negative_tests_validation_pass": semantic_negative_tests_pass,
        "failed_semantic_negative_tests": failed_semantic_negative_tests,
        "no_overclaim_validation_pass": not forbidden_hits,
        "forbidden_hits": forbidden_hits,
        "token_boundary_validation_pass": metrics.get("token_boundary_violations") == 0,
        "regulated_boundary_validation_pass": metrics.get("regulated_boundary_violations") == 0,
        "replay_validation_pass": metrics.get("replay_pass") is True and replay_report.get("replay_pass") is True,
        "replay_report_pass": replay_report.get("replay_pass") is True,
        "freeze_validation_pass": bool(metrics.get("capability_hashes")) and metrics.get("capabilities_frozen") == metrics.get("capabilities_generated"),
        "safety_validation_pass": not safety_nonzero,
        "safety_nonzero": safety_nonzero,
        "public_status_consistent": support_consistent,
    }
    result["validation_pass"] = all(v is True for k, v in result.items() if k.endswith("_pass")) and support_consistent
    return result
