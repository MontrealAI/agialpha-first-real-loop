# AGI ALPHA ENGINE-001

AGI ALPHA ENGINE-001 is a **proof-gated recursive experiment engine** that runs fully local, deterministic, repo-owned self-improvement cycles.

## What this engine is

- A bounded engine that discovers improvement opportunities from local repo context.
- A Task Foundry that proposes candidate tasks with validator specs, solver/patch plans, replay plans, and Evidence Docket plans.
- A safe local evaluator that compares baseline variants (B0–B7), runs ablations, and computes vRCI.
- A provenance-producing pipeline that emits ProofBundles, Evidence Dockets, replay/falsification artifacts, archive entries, and descendant task candidates.
- A human-governed promotion path: autonomous evidence production is allowed; autonomous promotion is not.

## What this engine is not

- Not a claim that AGI/ASI/superintelligence has been achieved.
- Not an empirical SOTA or official benchmark victory claim.
- Not a certification, legal/compliance exemption, or guaranteed security/economic outcome.
- Not a payment/custody/trading system; $AGIALPHA remains utility-only accounting in this implementation.

## Quick run commands

```bash
python -m agialpha_engine discover --repo-root . --registry engine_registry
python -m agialpha_engine run-cycle --repo-root . --registry engine_registry --out /tmp/agialpha-engine-test --candidate-tasks 16 --evaluate-tasks 6 --variants-per-task 2
python -m agialpha_engine evaluate-baselines --repo-root . --run /tmp/agialpha-engine-test
python -m agialpha_engine run-ablations --repo-root . --run /tmp/agialpha-engine-test
python -m agialpha_engine replay --run /tmp/agialpha-engine-test
python -m agialpha_engine falsification-audit --run /tmp/agialpha-engine-test
python -m agialpha_engine validate --run /tmp/agialpha-engine-test
python -m agialpha_engine build-data --registry engine_registry --out docs/_generated/agialpha-engine
```

## How to inspect results

- Per-run artifacts: `/tmp/agialpha-engine-test/` or `engine_registry/runs/<run_id>/`
- Registry indexes: `engine_registry/*.json`
- Generated route data: `docs/_generated/agialpha-engine/*.json`
- Public docs: `docs/agialpha-engine/`

## Baselines (B0–B7)

- B0 no engine, B1 static checklist, B2 CI-only, B3 evidence-wrapper only,
- B4 task generator without validators,
- B5 validators without archive reuse,
- B6 full engine,
- B7 human-promoted improvement (pending without explicit human record).

Core comparison is **B6 vs B5** under equal local constraints.

## vRCI computation (Verified Recursive Capability Improvement)

vRCI summarizes held-out-valid improvement plus archive/validator/replay/evidence gains, minus penalties for cost/safety/boundary/replay/fake-metric failures.

If a component metric is missing, it is reported explicitly (for example `not_reported`, `pending`, `unavailable`, or `skipped_with_reason`) and never silently coerced to zero.

## Archive reuse and descendant generation

Accepted and rejected artifacts are preserved append-only in archive registries. Descendant task generation reuses archived capability metadata to propose next-step work while preserving human review gates.

## Human review and persistence controls

Every major artifact enforces:

- `human_review_required: true`
- `no_auto_merge: true`
- `autonomous_persistence_allowed: false`

Promotion to vNext candidates is therefore human-reviewed promotion required.

## Why this differs from hype

ENGINE-001 emphasizes **local bounded public evidence** and **implementation-side evidence** over unverified claims. It is a deterministic proof-gated recursive experiment engine with explicit claim, token, and regulated-boundary controls.
