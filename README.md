# AGI ALPHA First Real Loop

**Evidence Factory, Replay Portal, and Mission Control for AGI ALPHA’s proof-bearing machine-labor experiments.**

This repository turns AGI ALPHA’s architecture into replayable Evidence Dockets: workflows that run real or proxy tasks, compare baselines, emit ProofBundles, record cost/safety ledgers, publish scoreboards, and preserve claim boundaries.

> [!WARNING]
> This repository records bounded Evidence Docket experiments. It does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, official public benchmark victory, or civilization-scale capability.

## Quick links
| Area | Link |
|---|---|
| Evidence Mission Control | [README_EVIDENCE_HUB.md](README_EVIDENCE_HUB.md) |
| Workflow Launchpad | [WORKFLOW_LAUNCHPAD.md](WORKFLOW_LAUNCHPAD.md) |
| Experiments | [README_EXPERIMENTS.md](README_EXPERIMENTS.md) |
| Run from GitHub UI | [docs/QUICKSTART_GITHUB_UI.md](docs/QUICKSTART_GITHUB_UI.md) |
| External replay | [docs/EXTERNAL_REPLAY.md](docs/EXTERNAL_REPLAY.md) |
| Claim levels | [docs/CLAIM_LEVELS.md](docs/CLAIM_LEVELS.md) |
| Safety boundaries | [docs/SECURITY_BOUNDARIES.md](docs/SECURITY_BOUNDARIES.md) |
| Developer guide | [README_DEVELOPERS.md](README_DEVELOPERS.md) |

## What this repo does
- Runs autonomous experiments and replay workflows.
- Produces Evidence Dockets and ProofBundles.
- Compares AGI ALPHA runs against baselines.
- Publishes public Evidence Hub pages via a central publisher only.

## How to run from GitHub UI
1. Open **Actions**.
2. Choose a workflow (see [WORKFLOW_LAUNCHPAD.md](WORKFLOW_LAUNCHPAD.md)).
3. Click **Run workflow**.
4. Keep defaults unless docs specify otherwise.
5. Wait for a green check.
6. Open artifacts.
7. Run/poll Evidence Hub publisher.
8. Read claim level and safety ledger.

## Results pipeline
`workflow -> Evidence Docket -> artifact -> manifest -> registry -> Evidence Mission Control -> experiment page`

## Developer quickstart
```bash
python -m unittest discover -s tests
python -m agialpha_evidence_hub build --registry evidence_registry --out _site
python -m agialpha_evidence_hub validate --registry evidence_registry --site _site
```

## Experiment families
First RSI Loop / ColdChain-Energy-Loop-001, Evidence Factory, HELIOS, Cyber Sovereign, Benchmark Gauntlet, OMEGA/OMEGA-AEGIS, Phoenix Hub, replay, falsification, scaling.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## RSI-GOVERNOR-001

RSI-GOVERNOR-001 tests whether AGI ALPHA can modify the mechanism that governs future evidence work, prove the modification improves held-out future-work performance, and persist the improvement only through Evidence Docket and human-reviewed PR promotion.

## AGI-GA Foundry
AGI-GA Foundry is a proof-gated open-ended directed evolution engine for sovereign work capabilities. Public page: `agiga-foundry/index.html`.


## α-AGI Protocol Cybersecurity Sovereign

Defensive, proof-gated cybersecurity sovereign for repo-owned work. See `/cybersecurity-sovereign/`.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
