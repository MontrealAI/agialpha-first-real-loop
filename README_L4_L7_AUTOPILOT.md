# AGI ALPHA L4-L7 Evidence Autopilot v0.1

This package adds an autonomous evidence layer to `MontrealAI/agialpha-first-real-loop`.

It targets:

- **L4** — external reviewer replay readiness, with a clean reviewer workflow and attestation kit.
- **L5** — baseline-comparative local real-task evidence using B0-B4 baselines.
- **L6** — agent/node scaling matrix evidence in CI-proxy form.
- **L7** — real-task portfolio Evidence Dockets across multiple bounded task families.

## Claim boundary

This package does **not** claim achieved AGI, ASI, empirical SOTA, safe autonomy, standard-setting control, guaranteed economic return, or civilization-scale capability. It creates autonomous Evidence Dockets and scoreboards that make claims harder to dismiss while keeping claim levels conservative.

## Workflows

Copy these from `COPY_WORKFLOWS` into `.github/workflows/` using GitHub web UI:

- `l4-l7-evidence-autopilot.yml`
- `l4-external-reviewer-replay.yml`

## Main workflow

Run:

`Actions → AGI ALPHA L4-L7 Evidence Autopilot → Run workflow`

This generates:

- per-task Evidence Dockets
- L5 baseline summaries
- L6 scaling matrix
- L4 external reviewer kit
- replay report
- falsification audit
- GitHub Pages scoreboard

## External reviewer workflow

An outside reviewer should fork the repo and run:

`Actions → AGI ALPHA External Reviewer Replay / L4 → Run workflow`

They should download the artifact, complete the attestation, and submit it by PR or issue.
