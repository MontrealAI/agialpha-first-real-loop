# Experiment Guide

Use this page to understand each experiment family, what it is allowed to claim, what to run, and where outputs appear.

## How to read this guide
For each family, this guide lists:
- **Purpose**
- **Safe claim**
- **Boundary**
- **Workflows**
- **Artifacts**
- **Public page**
- **Success/failure interpretation**

> If a metric or benchmark claim is not documented in an Evidence Docket and replay path, treat it as pending.

## First Real Loop / ColdChain
- **Purpose:** deterministic first-loop evidence production and handoff.
- **Safe claim:** local evidence run completed with bounded artifacts.
- **Boundary:** not AGI/ASI proof, not unsupported performance by default.
- **Workflows:** see `seed-runner-autonomous.yml`, related replay/falsification flows in `docs/WORKFLOW_CATALOG.md`.
- **Artifacts:** Evidence Docket, replay instructions, safety/cost ledgers, hash manifest.
- **Public page:** Evidence Mission Control.
- **Success:** reproducible bounded output.
- **Failure:** missing artifacts, failed replay, or failed guardrails.

## Evidence Factory
- **Purpose:** autonomous evidence packaging and publication handoff.
- **Safe claim:** autonomous evidence production pipeline executed.
- **Boundary:** autonomous claim promotion is forbidden.
- **Workflows:** `evidence-factory-autonomous.yml`, `falsification-audit-autonomous.yml`, `independent-replay-autonomous.yml`.
- **Artifacts:** ProofBundle, manifest, Evidence Docket slices.
- **Public page:** `docs/evidence-factory/index.html` and mission control pages.

## HELIOS (001–004)
- **Purpose:** experiment family for autonomous runs, replay, falsification, scaling, and transfer stages.
- **Safe claim:** scoped HELIOS run produced local evidence and boundary checks.
- **Boundary:** no unsupported capability promotion.
- **Workflows:** `helios-001-*`, `helios-002-*`, `helios-003-*`, `helios-004-completion.yml`.
- **Artifacts:** family-specific manifests and dockets.
- **Public page:** HELIOS docs and mission control index.

## Cyber Sovereign + Cyber-GA Sovereign
- **Purpose:** defensive cyber-governance experimentation with evidence-led remediation pathways.
- **Safe claim:** defensive governance and proof-bound remediation run completed.
- **Boundary:** not offensive cyber capability, not cybersecurity approval.
- **Workflows:** `cyber-sovereign-*`, `cyber-ga-sovereign-*` lifecycle/replay/falsification/safe PR workflows.
- **Artifacts:** safety ledger, remediation proposals, Evidence Docket, replay logs.
- **Public page:** family docs + mission control run pages.

## AGI-GA Foundry
- **Purpose:** foundry lifecycle for governed generation, replay, policy PRs, and vNext promotion candidates.
- **Safe claim:** governed generation/review workflow completed with evidence.
- **Boundary:** no autonomous claim promotion.
- **Workflows:** `agiga-foundry-001-*` set.
- **Artifacts:** lifecycle manifests, policy artifacts, dockets.

## RSI Governor / RSI Forge
- **Purpose:** candidate generation and lifecycle governance with replay/falsification and promotion gates.
- **Safe claim:** bounded lifecycle evidence generated and reviewed.
- **Boundary:** no automatic merge or unchecked promotion.
- **Workflows:** `rsi-governor-001-*`, `rsi-forge-001-*`, `rsi-forge-002-*`.
- **Artifacts:** candidate logs, safety counters, replay/falsification outputs.

## Benchmark Gauntlet / Omega / Phoenix / Ascension
- **Purpose:** challenge-pack and independent replay-heavy experiment branches.
- **Safe claim:** run completed with challenge-pack evidence and bounded evaluation records.
- **Boundary:** no unsupported benchmark-win claim without required external evidence tier.
- **Workflows:** `benchmark-gauntlet-001-*`, `omega-gauntlet-001-*`, `omega-aegis-001-*`, `phoenix-hub-001-*`, `ascension-001-*`.
- **Artifacts:** challenge packs, replay artifacts, falsification reports, dockets.

## Evidence Mission Control / Autopublisher
- **Purpose:** central discovery and publication layer.
- **Safe claim:** docs index/publishing pipeline updated.
- **Boundary:** central publisher is required; avoid ad hoc Pages deploy workflows.
- **Workflows:** `evidence-hub-publish.yml`, `evidence-hub-canary.yml`, `evidence-hub-repair.yml`.

## Canonical references
- `docs/WORKFLOW_CATALOG.md`
- `docs/EVIDENCE_GUIDE.md`
- `docs/EVIDENCE_MISSION_CONTROL.md`
- `docs/CLAIM_BOUNDARIES.md`
