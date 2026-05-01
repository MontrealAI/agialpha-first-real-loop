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
