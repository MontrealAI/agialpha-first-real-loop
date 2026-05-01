# AGI ALPHA Evidence Hub Operations Guide

## Why central publishing is required
GitHub Pages serves a complete static snapshot, so per-workflow deployments can overwrite prior evidence.
This repository now uses a **single publisher workflow** (`.github/workflows/evidence-hub-publish.yml`) that rebuilds and deploys one complete hub from durable registry data.

## Evidence emission from experiment workflows
Experiment workflows keep their scientific/runtime logic, but they must:
1. Emit `evidence-run-manifest.json` via `python -m agialpha_evidence_hub emit-manifest`.
2. Upload the manifest plus dockets/scoreboards/replay/safety/cost artifacts.
3. Never deploy Pages directly.
4. Optionally dispatch `repository_dispatch` (`evidence_run_completed`) to trigger central rebuild.

## Persistent registry model
Registry state is stored in `evidence_registry/` and preserved across runs, including when artifacts later expire.
Important files:
- `evidence_registry/runs.json`
- `evidence_registry/experiments.json`
- `evidence_registry/workflows.json`
- `evidence_registry/latest.json`
- per-experiment and per-run JSON under `evidence_registry/experiments/**`

## Dynamic discovery for future autonomous experiments
Discovery is intentionally multi-path:
- manifest scan
- repository path scan (docs, dockets, autonomous outputs, gauntlet/sovereign families)
- workflow YAML scan
- Actions run metadata scan
- artifact ingest scan
- historical backfill scan

This prevents hardcoding to current families and supports newly created autonomous experiments.

## Common operator commands
- Discover: `python -m agialpha_evidence_hub discover --repo-root . --out evidence_registry/discovered.json`
- GitHub runs: `python -m agialpha_evidence_hub github-discover --registry evidence_registry --limit 500`
- Backfill: `python -m agialpha_evidence_hub backfill --repo-root . --registry evidence_registry`
- Register a run: `python -m agialpha_evidence_hub register-run --input <manifest_or_docket_dir> --registry evidence_registry`
- Build site: `python -m agialpha_evidence_hub build --registry evidence_registry --out _site`
- Validate site: `python -m agialpha_evidence_hub validate --registry evidence_registry --site _site`
- Link check: `python -m agialpha_evidence_hub linkcheck --site _site`

## Manual central publisher trigger
- GitHub UI: run `.github/workflows/evidence-hub-publish.yml` with `workflow_dispatch`.
- API/CLI: send `repository_dispatch` type `evidence_run_completed`.

## Handling historical runs and missing data
If older runs lack complete manifests, backfill creates conservative entries with explicit statuses such as
`pending`, `unavailable`, `not_reported`, `artifact_expired`, `discovered_without_manifest`, or `backfill_required`.
No metrics are invented.

## Debugging missing runs
1. Confirm workflow emitted and uploaded `evidence-run-manifest.json`.
2. Check `evidence_registry/discovered.json` and `evidence_registry/runs.json`.
3. Run backfill/discover/github-discover locally.
4. Rebuild `_site` and inspect generated `/_site/data/*.json`.

## Claim levels and overclaim policy
Claim levels are bounded evidence labels (e.g., `L3`, `L4-ready`, `L6-CI-proxy`, `pending`, `historical-local`)
and are governed by schema and safety validation. Unsafe positive claims are rejected unless clearly negated
in claim-boundary context.

## Artifact expiration handling
The registry keeps run metadata even if artifacts expire. Expired artifact links remain visible with explicit
status messaging rather than silent deletion.

## Content Preservation / Migration Notes
- Legacy experiment routes (e.g., `/helios-001/`, `/cyber-sovereign-002/`) are preserved and mapped to canonical summaries when data exists.
- Historical placeholder pages are replaced by bounded summaries with explicit missing-data states when evidence is partial.
- Existing richer evidence pages are preserved and not downgraded to generic placeholders.

## Claim boundary
No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.


See also: [`CONTENT_PRESERVATION_MIGRATION_NOTES.md`](CONTENT_PRESERVATION_MIGRATION_NOTES.md).

## Strict Prompt Profile (Mission Control Hard Mode)

For large-scale Codex migrations, enforce these invariants explicitly in the prompt:

- **No evidence downgrade:** lower-information backfill must never overwrite richer manifests/scoreboards.
- **Project-path-safe assets:** nested pages must resolve `/agialpha-first-real-loop/assets/app.css` and `app.js`.
- **Single Pages deployer:** only `evidence-hub-publish.yml` may publish GitHub Pages.
- **Rich experiment pages required:** if evidence exists, render metrics/safety/replay tables (no shallow placeholders).
- **Workflow launch controls:** per-workflow GitHub UI links and copyable `gh workflow run ...` commands only (no browser tokens).
- **Persistent registry first:** preserve run history, artifacts, raw references, and conflict notes in `evidence_registry/CHANGELOG.md`.
- **Claim boundary doctrine:** every page must include `No Evidence Docket, no empirical SOTA claim.`

This profile keeps the site operator-friendly while preserving publication-grade evidence discipline.

