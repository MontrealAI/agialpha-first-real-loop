# AGI ALPHA HELIOS-002 v0.1

**Experiment 56: HELIOS-002 — External Transfer and Reviewer Replay for Governed Compounding of Verified Machine Labor**

HELIOS-002 tests whether the reusable capability created in HELIOS-001, `EnergyComputeResilienceCompiler-v0`, transfers to harder adjacent task families while beating no-reuse and simpler baselines under replay, cost, safety, and audit constraints.

## What this package adds

- `agialpha_helios2` Python module
- HELIOS-002 autonomous experiment workflow
- HELIOS-002 external reviewer replay workflow
- HELIOS-002 scaling workflow
- HELIOS-002 falsification audit workflow
- HELIOS-002 public benchmark adapter workflow
- External review issue template

## Evidence levels

- **L4-ready:** external reviewer kit and replay workflow exist.
- **L5-local:** bounded local/proxy baseline-comparative transfer evidence.
- **L6-CI-proxy:** scaling matrix over agents and node proxies; physical node scaling is not claimed.
- **L7-local:** local HELIOS-002 transfer portfolio.

## Claim boundary

This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, standard-setting control, guaranteed economic return, real-world energy savings, or civilization-scale capability. It tests whether a reusable verified capability from HELIOS-001 transfers to harder tasks under baselines, replay, safety ledgers, cost ledgers, and external review. Stronger claims require external reviewer replay, stronger public benchmarks, delayed outcomes, and independent audit.

## Local run

```bash
python -m agialpha_helios2 run --out runs/helios-002/local --source evidence-docket --docs docs
python -m agialpha_helios2 external-replay --out runs/helios-002-external/local --source runs/helios-002/local
python -m agialpha_helios2 scaling --out runs/helios-002-scaling/local --docs docs
python -m agialpha_helios2 audit --out runs/helios-002-audit/local --source runs/helios-002/local
python -m agialpha_helios2 adapters --out runs/helios-002-adapters/local --docs docs
```

## Web UI install summary

Upload these visible items:

- `agialpha_helios2`
- `config`
- `tests`
- `COPY_WORKFLOWS`
- `COPY_ISSUE_TEMPLATES`
- `README_HELIOS_002.md`

Then manually create workflow files from `COPY_WORKFLOWS`:

- `.github/workflows/helios-002-autonomous.yml`
- `.github/workflows/helios-002-external-replay.yml`
- `.github/workflows/helios-002-scaling.yml`
- `.github/workflows/helios-002-falsification-audit.yml`
- `.github/workflows/helios-002-benchmark-adapters.yml`

Optional issue template:

- `.github/ISSUE_TEMPLATE/helios-002-external-review.md`

Run `AGI ALPHA HELIOS-002 / Autonomous` first.
