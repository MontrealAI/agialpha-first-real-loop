# AGI ALPHA Edge Runner v0.2

This package pushes the current Evidence Factory one layer further:

```text
Edge Seed Runner -> Independent Replay -> Falsification Audit -> GitHub Pages scoreboards
```

It is designed for `MontrealAI/agialpha-first-real-loop`.

## What it adds

- Completed seed Evidence Docket scaffolds for seed-001 through seed-010.
- Separate autonomous Independent Replay workflow.
- Separate autonomous Falsification Audit workflow.
- Conservative claim-level gating.
- External reviewer kit for each docket.
- Scoreboards for seed dockets, independent replay, and falsification audit.

## Claim boundary

Autonomous evidence generation is allowed; autonomous claim promotion is not. This package does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, standard-setting control, guaranteed economic return, or civilization-scale capability. Stronger claims require external independent replay, full baselines, cost/safety ledger review, delayed outcomes, and independent audit.

## Web UI install summary

Upload these visible folders/files first:

```text
agialpha_seed_runner
config
tests
COPY_WORKFLOWS
README_EDGE_RUNNER.md
```

Then create these workflow files manually from `COPY_WORKFLOWS`:

```text
.github/workflows/seed-runner-autonomous.yml
.github/workflows/independent-replay-autonomous.yml
.github/workflows/falsification-audit-autonomous.yml
```

Run `AGI ALPHA Edge Seed Runner / Autonomous` from the Actions tab. The Independent Replay and Falsification Audit workflows should chain automatically.
