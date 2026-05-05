# Operator Guide (GitHub UI)

Use this guide when running repository workflows from the GitHub web interface.

## 1) Open Actions
1. Open the repository on GitHub.
2. Click the **Actions** tab.
3. Select a workflow from `docs/WORKFLOW_LAUNCHPAD.md` or `docs/WORKFLOW_CATALOG.md`.

<!-- screenshot placeholder: actions-tab-overview -->

## 2) Select workflow and click Run workflow
1. Choose the workflow page.
2. Click **Run workflow** (top-right).
3. Choose branch/ref.
4. Fill `workflow_dispatch` inputs.
5. Click **Run workflow** to submit.

<!-- screenshot placeholder: run-workflow-dialog -->

## 3) Understand workflow inputs
Common input meanings:
- `ref`/`branch`: code revision to run.
- `mode`/`profile`: bounded run profile.
- `seed`/`pack`: deterministic test data selector.
- `publish`: whether output is sent to central publishing flow.

Use documented defaults unless a runbook says otherwise.

## 4) Inspect logs and status
- Open each job/step for detailed logs.
- Validate safety checks, replay checks, and claim-boundary checks.
- Green = checks passed for run scope.
- Red = failed check; follow `docs/TROUBLESHOOTING.md`.

## 5) Download artifacts
1. Open run summary.
2. In **Artifacts**, download the output bundle.
3. Confirm expected files exist (manifest, replay files, ledgers, Evidence Docket).

## 6) Find Evidence Dockets and safety ledgers
- Evidence Docket location is workflow-specific; use artifact manifest and run logs.
- Safety ledger and cost ledger should be present for bounded security/evidence workflows.
- If missing, treat run as incomplete.

## 7) Interpret pass/fail conservatively
- **Pass**: bounded workflow checks passed.
- **Fail**: run failed or guardrail blocked execution.
- Neither status alone authorizes capability overclaims.

## 8) Rerun jobs safely
- Use **Re-run failed jobs** for transient failures.
- Do not rerun to bypass policy gates.
- Keep notes in run comments or issue tracker for auditability.

## 9) Review safe PR proposals
- Safe PR proposals still require human review.
- Verify diff scope, safety counters, claim boundary language, and artifact integrity.
- Avoid accidental merges; never auto-merge unsafe remediation.

## 10) Trigger Evidence Mission Control / Autopublisher
- Use central publisher workflows only (`evidence-hub-publish` path).
- Do not create side-channel Pages deploy workflows.
- Validate publish logs and resulting page references.

## 11) If Pages does not update
1. Check latest `evidence-hub-publish` run status.
2. Confirm permissions and token scope.
3. Confirm artifacts contain expected publish payload.
4. Re-run publish workflow once root cause is fixed.

## Boundary reminder
SecureRails is governance + defensive remediation, not autonomous certification or offensive cyber. `$AGIALPHA` is utility accounting infrastructure only.
