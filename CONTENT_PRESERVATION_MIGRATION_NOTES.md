# Content Preservation / Migration Notes

This repository now uses a **single central publisher** workflow for GitHub Pages:

- `.github/workflows/evidence-hub-publish.yml`

All legacy experiment workflows remain runnable and keep experiment/artifact logic, but Pages deployment is centralized so historical evidence is not overwritten by independent workflow deploys.

## Preservation model

- Durable run metadata is recorded in `evidence_registry/`.
- Historical runs are preserved in registry indexes and per-experiment run folders.
- Artifact IDs and names are retained even when artifact availability later transitions to `expired`.
- Source precedence is deterministic (manifest-first), with changelog notes for conflicts.

## Migration safeguards

- `scripts/check_pages_architecture.py` enforces that only the central publisher may deploy Pages.
- Experiment workflows are expected to emit `evidence-run-manifest.json` and upload it as an artifact.
- Legacy routes are generated and linked to canonical experiment pages so previously shared URLs remain useful.

## Backfill behavior

Backfill is conservative:

- If exact metrics are unavailable, values are marked `pending`, `unavailable`, or `not_reported`.
- No metrics are fabricated.
- Claim boundaries are preserved and rendered across public pages.

## Claim boundary (global)

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
