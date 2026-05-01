# Non-Technical Operator Guide

This guide is for operators using only the GitHub web UI.

## Run a workflow

1. Go to the repository **Actions** tab.
2. Select a workflow from the left panel.
3. Click **Run workflow**.
4. Keep default branch as `main` unless directed otherwise.
5. Submit and wait for a green check.

## Check evidence output

1. Open the completed run.
2. Download artifacts.
3. Open the public Evidence Mission Control page.
4. Confirm the run appears in Recent Runs and experiment pages.
5. Confirm claim boundary banner is visible.

## If a workflow fails

- Open logs for the failed job.
- Confirm required inputs were provided.
- Check artifact upload steps executed.
- Re-run workflow once after fixing obvious input/branch mistakes.
- If still failing, open a bug issue with run URL and screenshot.

## If Pages does not update

- Run `evidence-hub-publish` from Actions on `main`.
- Confirm build/validate/linkcheck jobs pass.
- Confirm deploy job runs only from trusted `main` events.

## Required policy reminder

**No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.**
