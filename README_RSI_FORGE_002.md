# AGI ALPHA RSI-FORGE-002

## Self-Amending Evidence Kernel for Governed Recursive Self-Improvement

This experiment is intentionally stronger than another dashboard, security scan, or local benchmark. It tests whether AGI ALPHA can improve the governance mechanism that decides future evidence-producing work.

The core RSI loop is:

```text
TARGET -> EMIT -> FILTER -> ATLAS -> TEST-PLAN -> EVAL -> INSERT -> PROMOTE
```

The experiment runs multiple recursive cycles. In each cycle, the system generates candidate EvidenceKernel variants, evaluates them against B0-B6 baselines, applies replay/safety/evidence gates, appends ECI events, creates Move-37 dossiers for high-novelty improvements, promotes only validated kernels, and writes an append-only state hash chain.

## What makes this strong RSI

RSI-FORGE-002 does not merely solve a task. It improves the policy kernel that will decide future tasks.

```text
prior kernel/state
-> candidate self-amendments
-> baseline-comparative evaluation
-> replay and safety gates
-> ECI ledger
-> Move-37 dossier if novelty + advantage
-> promoted kernel
-> safe PR for human-governed persistence
-> next run starts from improved kernel/state
```

The decisive comparison is:

```text
B5 = AGI ALPHA RSI without archive/state reuse
B6 = RSI-FORGE with persisted kernel + archive reuse
```

The vNext test asks whether the improved kernel transfers to held-out future evidence-governance tasks.

## Claim boundary

This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, or civilization-scale capability. It is a bounded, repo-owned RSI Evidence Docket experiment testing whether a schema-bound, replayable, baseline-comparative kernel can improve its own future evidence-production policy under drift sentinels, ECI gates, ProofBundles, safety ledgers, and human-governed promotion.

## Files in this package

```text
rsi_forge_002/                         Python experiment engine
.github/workflows/rsi-forge-002-*.yml  Autonomous, replay, and falsification workflows
COPY_WORKFLOWS/                        Workflow files for easy GitHub web upload
config/rsi_forge_002_config.json       Experiment config
schemas/rsi_forge_002_manifest.schema.json
schemas/evidence_run_manifest.schema.json if you already maintain a shared hub schema
data/rsi_forge_002/current_kernel.json Initial EvidenceKernel policy
data/rsi_forge_002/latest_state.json   Initial RSI state with hash continuity
tests/test_rsi_forge_002.py            Unit tests
```

## Run locally

```bash
python -m rsi_forge_002 run --repo-root . --out /tmp/rsi-forge-002 --cycles 5 --candidates 18 --seed 37
python -m rsi_forge_002 replay --docket /tmp/rsi-forge-002
```

Open:

```text
/tmp/rsi-forge-002/scoreboard.html
```

## Run from GitHub web UI

1. Upload all package files into the repository root.
2. Go to **Actions**.
3. Open **AGI ALPHA RSI-FORGE-002 / Autonomous**.
4. Click **Run workflow**.
5. Keep defaults:
   - cycles: `5`
   - candidates: `18`
   - seed: `37`
   - create_policy_pr: checked
6. Wait for the green check.
7. Open the artifact named `rsi-forge-002-<run_id>`.
8. Open `scoreboard.html` inside the artifact.
9. Review the PR opened by the workflow. Do not merge automatically.

## How to continue the recursion

After reviewing the PR:

- If the Evidence Docket passes and the policy/state update is acceptable, merge the PR.
- Run **AGI ALPHA RSI-FORGE-002 / Autonomous** again.
- The next run will start from the improved kernel/state.

That is the governed recursion.

## External replay

After the autonomous run succeeds:

1. Copy the source run ID.
2. Open **AGI ALPHA RSI-FORGE-002 / Independent Replay**.
3. Paste the run ID.
4. Click **Run workflow**.
5. Confirm the replay artifact is uploaded.

## Falsification audit

1. Open **AGI ALPHA RSI-FORGE-002 / Falsification Audit**.
2. Paste the source run ID.
3. Click **Run workflow**.
4. If it fails, the claim must be downgraded.

## Promotion rule

RSI-FORGE-002 is locally promoted only if:

```text
B6 beats B5
B6 beats most baseline ladder conditions
vNext transfer beats B5
state hash continuity passes
ECI ledger is append-only
Move-37 dossiers are created when novelty + advantage triggers
replay passes
hard safety counters are all zero
human review is required before persistent policy promotion
```

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
