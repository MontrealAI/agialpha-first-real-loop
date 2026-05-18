# Workflow Launchpad Guide

The Evidence Hub Launchpad is the operator entry point for running repository workflows.

## What it provides

- Workflow catalog discovered from `.github/workflows`.
- Direct links to each workflow run page.
- Latest run status when available.
- Workflow dispatch availability and expected inputs.
- Copyable CLI commands (`gh workflow run <workflow-file>.yml`).

## Non-technical flow

1. Open the public Evidence Mission Control site.
2. Open **Launchpad**.
3. Click **Open Run Workflow Page** for the workflow you want.
4. In GitHub UI, click **Run workflow**.
5. Wait for completion, then return to the Evidence Hub to verify run ingestion.

## Safety and claim boundary

- Launchpad does **not** dispatch workflows from the browser.
- No tokens are embedded in site pages.
- Launchpad usage is bounded by the claim policy:  
  **No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.**

## SecureRails installable workflows
- SecureRails PR Guard Reusable Workflow: `.github/workflows/securerails-pr-guard-reusable.yml`
- SecureRails PR Guard Demo: `.github/workflows/securerails-pr-guard-demo.yml`
- Install docs: `docs/secure-rails/installable-action.md`
- Customer template: `docs/secure-rails/templates/customer-securerails-pr-guard.yml`

- Connector flow includes GitHub App webhook and repository_dispatch bridge.


- SecureRails E2E Pilot Canary 001: synthetic internal canary workflow.
- SecureRails E2E Pilot Canary Validate 001: validates canary output integrity and schema expectations.

## Recursive Gauntlet
Use lifecycle workflow to generate local bounded recursive substrate evidence.
\n- Enterprise Pilot: README_ENTERPRISE_PILOT.md and workflow agialpha-enterprise-pilot-001.yml

- AGI ALPHA Docs and Pages UX 001: `.github/workflows/agialpha-docs-pages-ux-001.yml`

- **AGI ALPHA Engine 002 / Measured Recursive Machine Labor Proof** — run `agialpha-engine-002-measured-recursive-proof.yml` for frozen-capability treatment/control proof artifacts. No direct Pages deploy or auto-merge.
