# AGI ALPHA BENCHMARK-GAUNTLET-001

## External Benchmark Evidence Docket for Scalable, Efficient, Safe Multi-Agent Coordination

This package implements the most convincing next experiment for the AGI ALPHA paper: a baseline-comparative, replayable, externally reviewable Evidence Docket that tests whether the full AGI ALPHA condition produces more verified work per cost than simpler baselines on real task schemas.

It is designed to satisfy the paper's evidence standard:

- real task manifests;
- B0-B6 baseline ladder;
- bounded execution;
- validator reports;
- ProofBundles;
- replay logs;
- cost ledgers;
- safety ledgers;
- α-WU calibration proxy;
- external reviewer kit;
- falsification audit;
- public scoreboard;
- external challenge pack path.

## What it tests

The central comparison is:

```text
B5 = AGI ALPHA + RSI without capability archive reuse
B6 = AGI ALPHA + RSI + capability archive reuse
```

The package also compares B6 against:

```text
B0 no agent
B1 static checklist
B2 fixed workflow
B3 unstructured swarm
B4 AGI ALPHA without RSI
```

## Task families

The default run includes these real task schemas:

1. software repair;
2. CI failure remediation;
3. data science workflow;
4. policy-bound tool use;
5. OpenAPI / ABI consistency;
6. docs / runbook consistency;
7. node runtime telemetry;
8. ProofBundle integrity;
9. redacted security hygiene.

External reviewers can add challenge packs under:

```text
external_challenge_packs/<reviewer-id>/challenge_pack.json
```

## Claim boundary

This experiment does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, standard-setting control, guaranteed economic return, real-world certification, or civilization-scale capability. It is a bounded, repo-owned, baseline-comparative Evidence Docket experiment testing whether AGI ALPHA can produce more replayable verified work per cost than simpler baselines on real task schemas. Stronger claims require external reviewer replay, official public benchmark execution, delayed outcomes, and independent audit.

## Local run

```bash
python -m agialpha_benchmark_gauntlet run --out runs/benchmark-gauntlet-001 --challenge-dir external_challenge_packs --docs-dir docs
python -m agialpha_benchmark_gauntlet replay --docket runs/benchmark-gauntlet-001/benchmark-gauntlet-001-evidence-docket
python -m agialpha_benchmark_gauntlet falsification-audit --docket runs/benchmark-gauntlet-001/benchmark-gauntlet-001-evidence-docket
```

## GitHub Actions workflows

Upload these files into `.github/workflows/`:

```text
benchmark-gauntlet-001-autonomous.yml
benchmark-gauntlet-001-external-replay.yml
benchmark-gauntlet-001-falsification-audit.yml
benchmark-gauntlet-001-challenge-pack.yml
benchmark-gauntlet-001-scaling.yml
benchmark-gauntlet-001-safe-pr.yml
```

Then run:

```text
Actions -> AGI ALPHA Benchmark Gauntlet 001 / Autonomous -> Run workflow
```

## Evidence Docket output

The generated docket contains:

```text
benchmark-gauntlet-001-evidence-docket/
  00_manifest.json
  01_claims_matrix.json
  02_environment.json
  03_task_manifests/
  04_baselines/
  05_agialpha_runs/
  06_proof_bundles/
  07_replay_logs/
  08_cost_ledgers/
  09_safety_ledgers/
  10_validator_reports/
  11_alpha_wu_calibration.json
  12_scaling_matrix.json
  13_external_reviewer_kit/
  14_falsification_audit.json
  15_summary_tables/
  16_challenge_pack_results/
  REPLAY_INSTRUCTIONS.md
  SCOREBOARD.html
```

## What success means

Correct claim if the workflow succeeds:

```text
BENCHMARK-GAUNTLET-001 demonstrates local, baseline-comparative, replayable Evidence Docket mechanics across multiple real task schemas. The full AGI ALPHA condition with RSI and archive reuse outperformed simpler local baselines under the docket's deterministic validators, cost ledger, safety ledger, replay, and falsification audit.
```

Do not say:

```text
AGI ALPHA achieved AGI.
AGI ALPHA achieved ASI.
AGI ALPHA is empirically SOTA.
AGI ALPHA is safe autonomous production infrastructure.
AGI ALPHA completed official public benchmark validation.
```

## Why this is the most convincing next experiment

Previous experiments demonstrated local compounding and defensive security organs. This gauntlet attacks the remaining reviewer objection: whether AGI ALPHA can convert its architecture into a reproducible, baseline-comparative Evidence Docket over multiple real task schemas, with external replay and challenge-pack hooks.

It is not the final proof. It is the experiment that turns the paper's standard into a public benchmark-shaped artifact.
