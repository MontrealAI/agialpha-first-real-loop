# Prompt for CODEX: AGI ALPHA Evidence Mission Control

This document captures a strict implementation prompt for transforming this repository into a dynamic, persistent, publication-grade AGI ALPHA Evidence Mission Control Center.

> Note: The canonical doctrine remains: **No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.**

## Full Prompt

Transform `MontrealAI/agialpha-first-real-loop` into an elite, dynamic, beautiful, persistent **AGI ALPHA Evidence Mission Control Center**.

Repository:

```text
https://github.com/MontrealAI/agialpha-first-real-loop
```

Current public site:

```text
https://montrealai.github.io/agialpha-first-real-loop/
```

### Objectives (condensed)

1. Dynamically discover experiments/workflows/runs.
2. Preserve evidence history and prevent overwrite races.
3. Enforce no-downgrade merging for rich evidence.
4. Render rich pages for root/experiments/workflows/runs.
5. Provide safe workflow launch controls (GitHub UI + gh CLI).
6. Maintain claim boundary language and overclaim guardrails.
7. Centralize GitHub Pages deployment into one workflow.
8. Build persistent registry + schema + validators + tests.
9. Ensure GitHub Pages project-path-safe assets under `/agialpha-first-real-loop/`.

### Architecture requirements (condensed)

- Python package: `agialpha_evidence_hub/` with discovery, ingest, build, validate, linkcheck, safety.
- Registry: `evidence_registry/` with runs/experiments/workflows indexes and changelog.
- Schema: `schemas/evidence_run_manifest.schema.json`.
- Site output: `_site/` with mission-control UI assets and rich route coverage.
- Launchpad: `/launchpad/` listing all workflows with run and dispatch guidance.
- Central publisher: `.github/workflows/evidence-hub-publish.yml` as **only** Pages deploy workflow.
- Check script: `scripts/check_pages_architecture.py` to block other deploy pathways.

### Safety and claim boundary invariants

- Never invent metrics.
- Never downgrade rich evidence with sparse backfill.
- Parse artifacts as data only; never execute artifact code.
- Escape artifact-derived content.
- Keep explicit claim-boundary text on every page.
- Reject unsafe positive claims unless explicitly negated within boundary context.

### Testing expectations (condensed)

- Unit tests for schema/discovery/backfill/build/links/legacy routes/sorting/no-overclaim/safety counters/launchpad/assets/pages architecture/no-rich-downgrade.
- Command checks:

```bash
python -m unittest discover -s tests
python scripts/check_pages_architecture.py
python -m agialpha_evidence_hub build --registry evidence_registry --out _site
python -m agialpha_evidence_hub validate --registry evidence_registry --site _site
python -m agialpha_evidence_hub linkcheck --site _site
```

### Deliverables summary

- `agialpha_evidence_hub/`
- `schemas/evidence_run_manifest.schema.json`
- `evidence_registry/` initial backfill
- `scripts/check_pages_architecture.py`
- `.github/workflows/evidence-hub-publish.yml`
- workflow manifest-emission migration updates
- mission-control UI assets + launchpad + legacy route backfills
- `README_EVIDENCE_HUB.md` + root README Evidence Mission Control section

### PR title requirement

```text
Build AGI ALPHA Evidence Mission Control
```

### Canonical invariant

```text
No Evidence Docket, no empirical SOTA claim.
Autonomous evidence production is allowed.
Autonomous claim promotion is not.
```
