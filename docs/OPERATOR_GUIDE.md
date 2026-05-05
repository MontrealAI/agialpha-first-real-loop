# Operator Guide (Non-Technical)

## What is this?
A governed experiment platform. You can run workflows, inspect artifacts, and review Evidence Dockets before any claim promotion.

## 10-minute path
1. Open Evidence Mission Control: `docs/EVIDENCE_MISSION_CONTROL.md`.
2. Open GitHub **Actions** tab.
3. Pick one workflow from `docs/WORKFLOW_LAUNCHPAD.md`.
4. Click **Run workflow**.
5. Wait for green check/red X.
6. Open logs and confirm expected steps ran.
7. Download artifacts.
8. Check the Evidence Docket and claim boundary text.
9. Confirm safety ledger and human review status.
10. Archive result and open/review PR manually.

## How to run from GitHub UI
- Repo → **Actions** → select workflow → **Run workflow**.
- Fill inputs exactly as documented.
- Never bypass required checks.

## How to know success
- Workflow status is green.
- Artifacts exist and are readable.
- Evidence Docket exists for empirical claims.
- Claim language remains bounded.

## How to respond if a workflow fails
- Open `docs/DEBUGGING_GUIDE.md`.
- Re-run only after fixing root cause.
- Do **not** merge with failing governance checks.

## Safe PR behavior
- Require manual review.
- Confirm no auto-merge path is introduced.
- Confirm no overclaim wording is added.

## Claim boundary, in plain language
- “Claim boundary” means: what we can responsibly claim from current evidence.
- “No Evidence Docket, no empirical SOTA claim” means: no benchmark superiority or frontier claim without the full evidence package.
