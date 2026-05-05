# Operator Guide (Non-Technical)

## What is this?
This repository runs bounded AI-agent experiment workflows and publishes reviewable evidence. You do not need to code to operate it safely, but you must follow governance checks before merging changes or promoting claims.

## Who is this for?
- Non-technical operators running GitHub workflows.
- PM/review owners validating artifacts and Evidence Dockets.

## What do I do first?
1. Open `docs/EVIDENCE_MISSION_CONTROL.md`.
2. Open `docs/WORKFLOW_LAUNCHPAD.md`.
3. Pick one workflow and read its expected artifacts in `docs/WORKFLOW_CATALOG.md`.

## 10-minute path
1. Open Evidence Mission Control.
2. Open GitHub **Actions**.
3. Run one workflow.
4. Inspect logs.
5. Inspect artifacts.
6. Check Evidence Docket.
7. Confirm claim boundary.
8. Confirm safety ledger.
9. Review PR manually.
10. Archive result.

## Run from GitHub UI
1. Open repository → **Actions** tab.
2. Click workflow name.
3. Click **Run workflow**.
4. Select branch + inputs exactly as documented.
5. Start run.

## How to verify success
- Green workflow status.
- Expected artifacts are present and downloadable.
- Evidence Docket is attached when empirical claims are discussed.
- Safety checks pass (claim boundary, no-auto-merge, safety ledger, use-case triage where applicable).

## How to read results
- **Evidence Mission Control**: top-level run index and experiment navigation.
- **Experiment page**: run summary, key outputs, links to evidence files.
- **Status badges/checks**: green = passed checks, red = block merge.
- **Evidence Docket**: what was tested, evidence scope, boundaries, and replay references.

## If a workflow fails
- Open `docs/DEBUGGING_GUIDE.md`.
- Fix root cause.
- Re-run workflow.
- Do not merge while governance checks fail.

## Safe PR behavior
- Open PR with clear summary of what changed.
- Require manual human review.
- Confirm no auto-merge behavior exists.
- Confirm wording remains claim-bounded.

## When not to merge
Do **not** merge if any of the following are true:
- Missing Evidence Docket for empirical claim language.
- Failed audit/check in Actions.
- Missing safety ledger where required.
- Overclaiming language (AGI/ASI/SOTA/certification/guarantee/investment framing).

## Claim boundary in plain language
- A claim boundary defines the strongest statement supported by current evidence.
- “No Evidence Docket, no empirical SOTA claim” means no benchmark-superiority claim without full docketed evidence and review.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
