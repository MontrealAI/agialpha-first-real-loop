# AGI ALPHA First Real Loop

AGI ALPHA First Real Loop is an evidence-first operating repository for running governed AI-agent experiments and publishing auditable results through Evidence Mission Control and SecureRails.

## 30-second orientation
- **Run workflows** from GitHub Actions or locally.
- **Review outputs** as ProofBundles, Evidence Dockets, safety ledgers, and replay artifacts.
- **Apply boundaries**: autonomous evidence production is allowed; autonomous claim promotion is not.
- **SecureRails outputs are advisory** and always require independent human validation before action.

## What this repository contains
- Evidence Mission Control and Evidence Hub publication flows
- SecureRails governance and compliance guardrails
- AGI-GA Foundry, Cyber-GA Sovereign, RSI Governor, HELIOS, and benchmark workflows
- Schemas, guard scripts, replay tooling, and audit checks

## Quickstart
- Start at `docs/quickstart/README.md`
- Workflow launchpad: `docs/workflows/README.md`
- Full docs hub: `docs/README.md`

## Where should I start?
| User | Start here | Goal |
|---|---|---|
| Non-technical operator | Quickstart + Workflow Launchpad | Run workflows safely |
| Engineer | Developer guide | Extend code and tests |
| Security reviewer | SecureRails + safety docs | Review defensive boundaries |
| Compliance reviewer | EU AI Act + misuse docs | Review deployment posture |
| External reviewer | Replay protocol | Reproduce evidence |
| Codex/agent developer | Agent contribution guide | Add experiments safely |

## Run from GitHub UI
1. Open **Actions**. 2. Select workflow. 3. Click **Run workflow**. 4. Choose branch + inputs. 5. Inspect checks and artifacts.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip pytest
python -m unittest discover -s tests
```

## Main systems
- Evidence Mission Control
- SecureRails
- AGI-GA Foundry
- Cyber-GA Sovereign
- RSI Governor
- Evidence Dockets
- ProofBundles

## Claim boundary
No Evidence Docket, no empirical SOTA claim. This repository does not claim achieved AGI/ASI, cybersecurity certification, guaranteed security, safe autonomy, autonomous production remediation, or investment returns.

## Engineering practices
- Document every workflow
- Keep schema-backed artifacts
- Preserve replayability and safety ledgers
- Keep no-automerge and human-review boundaries

## Documentation index
See `docs/README.md`.

## Troubleshooting
See `docs/quickstart/troubleshooting.md`.

## Quick links
- Docs hub: `docs/README.md`
- Workflow launchpad: `docs/workflows/README.md`
- Evidence docs: `docs/evidence/README.md`
- SecureRails docs: `docs/secure-rails/README.md`
- Work Vaults/MARK/Sovereigns: `docs/secure-rails/work-vaults-mark-sovereigns.md`

## How to run from GitHub UI
See `docs/quickstart/github-ui.md`.

## Experiment families
See `docs/experiments/README.md` for First Real Loop, HELIOS, Cyber Sovereign, Cyber-GA Sovereign, AGI-GA Foundry, RSI Governor, Benchmark Gauntlet, Omega, Phoenix, Ascension, replay, and falsification coverage.
