
# AGI ALPHA Seed Runner v0.1 + Independent Replay

This drop-in package adds two autonomous workflows to `MontrealAI/agialpha-first-real-loop`.

## What it does

1. **Seed Runner v0.1**
   - turns pending seeds into completed Evidence Docket scaffolds;
   - writes cost ledgers, safety ledgers, baseline scaffolds, replay reports, hash manifests, claim levels, and next-state files;
   - publishes a Seed Runner scoreboard;
   - uploads `seed-dockets` as a GitHub Actions artifact.

2. **Independent Replay**
   - runs in a separate GitHub Actions workflow;
   - downloads the Seed Runner artifact when available;
   - replays/validates each docket structurally in a clean workflow context;
   - uploads an `independent-replay-report` artifact.

## Claim boundary

Autonomous evidence generation is allowed. Autonomous claim promotion is not. These workflows do not claim AGI, ASI, empirical SOTA, safe autonomy, or broad scalability. Stronger claims require external reviewer replication, full baselines, measured cost/safety ledgers, delayed outcomes, and independent audit.

## Web UI install

Upload these folders/files through the GitHub web UI:

- `agialpha_seed_runner`
- `config/seed_runner_config.json`
- `tests/test_seed_runner.py`
- `README_SEED_RUNNER.md`

Then create two workflow files manually, because `.github` can be hidden on some computers:

- `.github/workflows/seed-runner-autonomous.yml`
- `.github/workflows/independent-replay-autonomous.yml`

Copy their content from the `COPY_WORKFLOWS` folder in this ZIP.
