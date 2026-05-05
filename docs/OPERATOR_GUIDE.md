# Operator Guide (GitHub UI)

## Run a workflow
1. Open repository **Actions** tab.
2. Select a workflow from `docs/WORKFLOW_CATALOG.md`.
3. Click **Run workflow**.
4. Fill `workflow_dispatch` inputs (branch, mode, flags).
5. Start run and monitor job logs.

<!-- screenshot placeholder: Actions tab workflow selection -->

## Inputs, logs, artifacts
- Inputs define run mode and scope; keep defaults unless runbook says otherwise.
- Logs show pass/fail and validator notes.
- Download artifacts from the run summary page.

## Evidence review flow
1. Find Evidence Docket and ProofBundle outputs.
2. Read replay log and safety ledger.
3. Check claim boundary in docs/claims output.
4. Treat as pending until human review is complete.

## Pass/fail interpretation
- Pass = bounded checks passed for this run.
- Fail = boundary or execution issue; use `docs/TROUBLESHOOTING.md`.

## Reruns and safe PR proposals
- Use **Re-run jobs** for transient issues.
- Review safe PR proposals manually; avoid accidental merges.

## Evidence Mission Control / Autopublisher
- Trigger publisher workflows only through documented central publisher flow.
- If Pages does not update, check `evidence-hub-publish` run logs and permissions.
