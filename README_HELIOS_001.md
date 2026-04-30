# AGI ALPHA HELIOS-001

**Project HELIOS — Governed Machine Labor for Energy-to-Compute Resilience**

This package adds an autonomous, baseline-comparative, replayable Evidence Docket experiment to `MontrealAI/agialpha-first-real-loop`.

## What it tests

HELIOS-001 tests whether governed verified machine labor can become a reusable capability, then improve future verified work. It is advisory-only and simulator/proxy-based. It does not control physical infrastructure.

## What it produces

The main workflow produces:

- six task Evidence Dockets;
- B0-B6 baseline comparisons;
- cost ledgers;
- safety ledgers;
- ProofBundles;
- replay logs;
- validator reports;
- alpha-WU proxy calibration;
- reuse and compounding analysis;
- `EnergyComputeResilienceCompiler-v0.json`;
- external reviewer kits;
- falsification audit;
- GitHub Pages scoreboard.

## Workflows

Create these files in `.github/workflows/` from `COPY_WORKFLOWS/`:

- `helios-001-autonomous.yml`
- `helios-001-independent-replay.yml`
- `helios-001-falsification-audit.yml`
- `helios-001-vnext-transfer.yml`

Run the first workflow manually once:

```text
Actions → AGI ALPHA HELIOS-001 / Autonomous → Run workflow
```

The others can run automatically after the main workflow completes, or manually.

## Claim boundary

This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, standard-setting control, guaranteed economic return, or civilization-scale capability. It records bounded Evidence Docket evidence. Stronger claims require external reviewer replay, stronger benchmarks, cost/safety ledger review, delayed outcomes, and independent audit.

## Local run

```bash
python -m agialpha_helios run --out runs/helios/local --publish-dir docs
python -m agialpha_helios replay --source runs/helios/local
python -m agialpha_helios audit --source runs/helios/local
python -m unittest discover -s tests
```
