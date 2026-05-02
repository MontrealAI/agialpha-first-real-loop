# RSI-GOVERNOR-001 Preflight Audit

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## rsi_governor_files
- `agialpha_rsi_governor/__init__.py`
- `agialpha_rsi_governor/__main__.py`
- `agialpha_rsi_governor/adversarial.py`
- `agialpha_rsi_governor/baselines.py`
- `agialpha_rsi_governor/canary.py`
- `agialpha_rsi_governor/candidate_lock.py`
- `agialpha_rsi_governor/candidates.py`
- `agialpha_rsi_governor/cli.py`
- `agialpha_rsi_governor/dossier.py`
- `agialpha_rsi_governor/drift.py`
- `agialpha_rsi_governor/eci.py`
- `agialpha_rsi_governor/evaluator.py`
- `agialpha_rsi_governor/falsification.py`
- `agialpha_rsi_governor/heldout_generator.py`
- `agialpha_rsi_governor/heldout_tasks.py`
- `agialpha_rsi_governor/kernel.py`
- `agialpha_rsi_governor/lifecycle.py`
- `agialpha_rsi_governor/overclaim.py`
- `agialpha_rsi_governor/promotion.py`
- `agialpha_rsi_governor/render.py`
- `agialpha_rsi_governor/replay.py`
- `agialpha_rsi_governor/safe_pr.py`
- `agialpha_rsi_governor/safety.py`
- `agialpha_rsi_governor/scoring.py`
- `agialpha_rsi_governor/state.py`
- `agialpha_rsi_governor/vnext_canary.py`

## governance_kernel_files
- `agialpha_governance_kernel/__init__.py`
- `agialpha_governance_kernel/claim_policy.py`
- `agialpha_governance_kernel/cli.py`
- `agialpha_governance_kernel/discovery_policy.py`
- `agialpha_governance_kernel/falsification_policy.py`
- `agialpha_governance_kernel/human_review_policy.py`
- `agialpha_governance_kernel/kernel.py`
- `agialpha_governance_kernel/page_quality_policy.py`
- `agialpha_governance_kernel/promotion_policy.py`
- `agialpha_governance_kernel/recommendation_policy.py`
- `agialpha_governance_kernel/registry_policy.py`
- `agialpha_governance_kernel/replay_policy.py`
- `agialpha_governance_kernel/safety_policy.py`
- `agialpha_governance_kernel/scoring_policy.py`
- `agialpha_governance_kernel/workflow_policy.py`

## workflows
- `.github/workflows/rsi-governor-001-autonomous.yml`
- `.github/workflows/rsi-governor-001-delayed-outcome.yml`
- `.github/workflows/rsi-governor-001-falsification-audit.yml`
- `.github/workflows/rsi-governor-001-lifecycle-orchestrator.yml`
- `.github/workflows/rsi-governor-001-lifecycle.yml`
- `.github/workflows/rsi-governor-001-post-merge.yml`
- `.github/workflows/rsi-governor-001-replay.yml`
- `.github/workflows/rsi-governor-001-safe-pr.yml`
- `.github/workflows/rsi-governor-001-vnext-canary.yml`

## tests
- `tests/test_rsi_governor_adversarial_tasks.py`
- `tests/test_rsi_governor_autonomy_contract.py`
- `tests/test_rsi_governor_baseline_comparison.py`
- `tests/test_rsi_governor_candidate_generation.py`
- `tests/test_rsi_governor_candidate_lock.py`
- `tests/test_rsi_governor_dossier.py`
- `tests/test_rsi_governor_drift_sentinel.py`
- `tests/test_rsi_governor_evidence_hub_integration.py`
- `tests/test_rsi_governor_executable_kernel.py`
- `tests/test_rsi_governor_falsification.py`
- `tests/test_rsi_governor_heldout_generation.py`
- `tests/test_rsi_governor_heldout_tasks.py`
- `tests/test_rsi_governor_helpers.py`
- `tests/test_rsi_governor_kernel_schema.py`
- `tests/test_rsi_governor_lifecycle.py`
- `tests/test_rsi_governor_lifecycle_orchestrator.py`
- `tests/test_rsi_governor_no_automerge.py`
- `tests/test_rsi_governor_no_overclaim.py`
- `tests/test_rsi_governor_post_merge.py`
- `tests/test_rsi_governor_promotion_gate.py`
- `tests/test_rsi_governor_replay.py`
- `tests/test_rsi_governor_safety_counters.py`
- `tests/test_rsi_governor_state_integrity.py`
- `tests/test_rsi_governor_vnext_canary.py`

