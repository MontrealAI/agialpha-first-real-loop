# Operator Quickstart

> For non-technical operators: use GitHub Actions + artifact downloads; do not edit code to run standard experiments.

## I want to run an experiment
- UI: Actions → workflow from [WORKFLOW_LAUNCHPAD](WORKFLOW_LAUNCHPAD.md) → Run workflow.
- CLI: `gh workflow run <workflow>.yml`
- Success: run completes and produces artifacts/Evidence Docket.
- Failure: missing input; fix by using documented workflow inputs.

## I want to replay evidence
- UI: run replay workflow and inspect replay report artifact.
- CLI: `gh workflow run <replay-workflow>.yml`
- Success: replay logs + deterministic match notes.
- Failure: expired artifact; re-run source workflow.

## I want to check SecureRails
- UI: open SecureRails workflows and compliance guard.
- CLI: `python scripts/secure_rails_claim_boundary_check.py .`
- Success: checks pass and no auto-merge violations.
- Failure: policy phrase violations; fix docs/workflow config, not by deleting guardrails.

## I want to inspect an Evidence Docket
- UI: download artifacts, open docket folder and `evidence-run-manifest.json`.
- CLI: inspect run outputs locally.
- Success: docket + manifest + claim boundary present.
- Failure: missing docket; run falsification/replay workflow and regenerate.

## I want to verify claim boundaries
- UI: inspect docs and workflow notes for explicit boundary statements.
- CLI: `python -m agialpha_docs audit-claims --repo-root .`
- Success: no forbidden positive overclaims.
- Failure: rewrite claims with negated boundary-safe language.

## I want to update Evidence Mission Control
- UI: run publish/repair workflow in Actions.
- CLI: `gh workflow run evidence-hub-publish.yml`
- Success: pages/index refreshes with latest artifacts.
- Failure: stale pages cache; run repair then publish.

## I want to add a new experiment
- Use [ADDING_NEW_EXPERIMENTS](ADDING_NEW_EXPERIMENTS.md).

## I want to know if it worked
- Check workflow status + artifacts + Evidence Docket + replay log + safety ledger + claim boundary.
