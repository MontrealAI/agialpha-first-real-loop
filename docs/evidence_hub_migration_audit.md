# Evidence Hub Migration Audit (source-of-truth)

Date: 2026-05-01

## 1) Workflows under `.github/workflows/`

All workflow files were enumerated directly from repository state:

- `ascension-001-autonomous.yml`
- `ascension-001-falsification-audit.yml`
- `ascension-001-independent-replay.yml`
- `ascension-001-vnext.yml`
- `benchmark-gauntlet-001-autonomous.yml`
- `benchmark-gauntlet-001-challenge-pack.yml`
- `benchmark-gauntlet-001-external-replay.yml`
- `benchmark-gauntlet-001-falsification-audit.yml`
- `benchmark-gauntlet-001-safe-pr.yml`
- `benchmark-gauntlet-001-scaling.yml`
- `cyber-sovereign-001-autonomous.yml`
- `cyber-sovereign-001-delayed-outcome.yml`
- `cyber-sovereign-001-external-replay.yml`
- `cyber-sovereign-001-falsification-audit.yml`
- `cyber-sovereign-001-scaling.yml`
- `cyber-sovereign-002-autonomous.yml`
- `cyber-sovereign-002-delayed-outcome.yml`
- `cyber-sovereign-002-external-replay.yml`
- `cyber-sovereign-002-falsification-audit.yml`
- `cyber-sovereign-002-safe-pr-proposal.yml`
- `cyber-sovereign-002-scaling.yml`
- `docs-audit.yml`
- `evidence-factory-autonomous.yml`
- `evidence-hub-publish.yml`
- `falsification-audit-autonomous.yml`
- `frontier-external-review.yml`
- `frontier-usefulness-autonomous.yml`
- `helios-001-autonomous.yml`
- `helios-001-falsification-audit.yml`
- `helios-001-independent-replay.yml`
- `helios-001-vnext-transfer.yml`
- `helios-002-autonomous.yml`
- `helios-002-benchmark-adapters.yml`
- `helios-002-external-replay.yml`
- `helios-002-falsification-audit.yml`
- `helios-002-scaling.yml`
- `helios-003-autonomous.yml`
- `helios-003-benchmark-adapters.yml`
- `helios-003-delayed-outcome.yml`
- `helios-003-external-replay.yml`
- `helios-003-falsification-audit.yml`
- `helios-003-scaling.yml`
- `helios-004-completion.yml`
- `independent-replay-autonomous.yml`
- `l4-external-reviewer-replay.yml`
- `l4-l7-evidence-autopilot.yml`
- `omega-aegis-001-autonomous.yml`
- `omega-aegis-001-external-replay.yml`
- `omega-aegis-001-falsification-audit.yml`
- `omega-aegis-001-vnext-transfer.yml`
- `omega-gauntlet-001-autonomous.yml`
- `omega-gauntlet-001-challenge-pack.yml`
- `omega-gauntlet-001-external-replay.yml`
- `omega-gauntlet-001-falsification-audit.yml`
- `omega-gauntlet-001-safe-pr.yml`
- `omega-gauntlet-001-scaling.yml`
- `phoenix-hub-001-autonomous.yml`
- `phoenix-hub-001-challenge-pack.yml`
- `phoenix-hub-001-external-replay.yml`
- `phoenix-hub-001-falsification-audit.yml`
- `phoenix-hub-001-safe-pr.yml`
- `replay.yml`
- `rsi-forge-001-autonomous.yml`
- `rsi-forge-001-falsification-audit.yml`
- `rsi-forge-001-independent-replay.yml`
- `rsi-forge-001-safe-pr.yml`
- `rsi-forge-001-vnext-transfer.yml`
- `rsi-forge-002-autonomous.yml`
- `rsi-forge-002-falsification-audit.yml`
- `rsi-forge-002-independent-replay.yml`
- `rsi-governor-001-autonomous.yml`
- `rsi-governor-001-delayed-outcome.yml`
- `rsi-governor-001-falsification-audit.yml`
- `rsi-governor-001-lifecycle.yml`
- `rsi-governor-001-post-merge.yml`
- `rsi-governor-001-replay.yml`
- `rsi-governor-001-safe-pr.yml`
- `rsi-governor-001-vnext-canary.yml`
- `seed-runner-autonomous.yml`

## 2) Which workflows currently deploy GitHub Pages

Only `.github/workflows/evidence-hub-publish.yml` contains Pages deployment actions (`actions/upload-pages-artifact`, `actions/deploy-pages`).

## 3) Which workflows emit artifacts

Most experiment and analysis workflows include `actions/upload-artifact` and/or docket outputs (confirmed by workflow catalog and existing `docs/**/runs/**/evidence-docket` payloads). Artifact-emitting families include HELIOS, Cyber Sovereign, Benchmark/Omega/Phoenix gauntlets, RSI Governor, RSI Forge, Ascension, replay, falsification, scaling, and external review.

## 4) Which workflows have `workflow_dispatch`

`workflow_dispatch` is broadly available and includes parameterized inputs for most workflows (validated through local workflow catalog generation in tests).

## 5) Which workflows are experiment producers

Autonomous producer workflows include: evidence-factory, seed-runner, frontier-usefulness, HELIOS-001/2/3/4, cyber-sovereign-001/002, benchmark-gauntlet-001, omega-gauntlet-001, phoenix-hub-001, rsi-governor-001, rsi-forge-001/002, ascension-001, omega-aegis-001.

## 6) Replay / falsification / scaling / delayed-outcome / external-review / safe-PR workflows

- Replay: `replay.yml`, `*-external-replay.yml`, `*-independent-replay.yml`, `rsi-governor-001-replay.yml`, `l4-external-reviewer-replay.yml`
- Falsification: `*-falsification-audit.yml`, `falsification-audit-autonomous.yml`
- Scaling: `*-scaling.yml`
- Delayed-outcome: `*-delayed-outcome.yml`
- External review: `frontier-external-review.yml`, `l4-external-reviewer-replay.yml`
- Safe-PR: `*-safe-pr.yml`, `cyber-sovereign-002-safe-pr-proposal.yml`

## 7) Existing evidence-related directories

`evidence_registry/`, `docs/evidence-factory/`, `rsi-governor-runs/`, `sample_outputs/`, plus multiple evidence/docket/replay/falsification/cost/safety files across `docs/` and run folders.

## 8) Existing docs / GitHub Pages outputs

Existing static docs include `docs/EVIDENCE_MISSION_CONTROL.md`, `docs/EVIDENCE_HUB_ARCHITECTURE.md`, experiment catalogs, security and claim-boundary docs, plus generated pages under `docs/evidence-factory/`.

## 9) Existing `evidence_registry`

Present with top-level JSON indexes and nested `evidence_registry/registry/*` snapshots (`registry.json`, `experiments.json`, `runs.json`, `workflows.json`, `latest.json`, `CHANGELOG.md`, `discovered.json`).

## 10) Broken, shallow, or placeholder pages

Historical shallow/seed-style routes exist in legacy docs patterns; resolver should keep them low-confidence unless manifests/workflow evidence exists.

## 11) Current public routes that must remain valid

Legacy experiment routes and mission-control routes expected by tests/docs include:
`/helios-001/`, `/helios-002/`, `/helios-003/`, `/helios-004/`, `/cyber-sovereign-001/`, `/cyber-sovereign-002/`, `/cyber-sovereign-003/`, `/benchmark-gauntlet-001/`, `/omega-gauntlet-001/`, `/phoenix-hub-001/`, `/rsi-governor-001/`, `/rsi-forge-001/`, `/ascension-001/`, `/evidence-factory/`, `/first-rsi-loop/`.

## 12) Known experiment families

First RSI Loop, Evidence Factory, HELIOS, Cyber Sovereign, Benchmark Gauntlet, Omega Gauntlet, Phoenix Hub, RSI Governor, RSI Forge, Ascension, independent replay/falsification/safety, external review.

## 13) Unknown discovered experiment families

Resolver can discover emergent families from workflow filenames, manifests, artifacts, and evidence paths containing keywords (`evidence`, `docket`, `gauntlet`, `sovereign`, `replay`, `benchmark`, `forge`, `governor`, `rsi`).

## 14) Current architectural failure mode

Historically, distributed per-workflow publishing and shallow backfill routing caused partial/overwritten public views. The required fix is strict central publishing, persistent registry normalization, confidence-ranked discovery, and conservative low-confidence isolation.
