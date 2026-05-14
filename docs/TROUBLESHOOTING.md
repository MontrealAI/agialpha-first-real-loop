# Troubleshooting

Use this format for every incident: **Symptom → Likely cause → Fix → What not to do**.

## Undocumented workflow
- **Symptom:** docs-audit fails with undocumented workflow errors.
- **Likely cause:** a new file was added under `.github/workflows/` without catalog update.
- **Fix:** add a row in `docs/WORKFLOW_CATALOG.md` and re-run docs tests.
- **What not to do:** do not disable workflow catalog tests.

## Missing script
- **Symptom:** workflow step fails with file-not-found.
- **Likely cause:** script path changed or file not committed.
- **Fix:** restore path/update workflow and add test coverage.
- **What not to do:** do not comment out safety-critical steps.

## Docs-claim failure / token language flagged
- **Symptom:** claim boundary checks fail for overclaim language.
- **Likely cause:** words implying AGI/ASI/SOTA/certification/investment returns.
- **Fix:** rewrite using `docs/CLAIM_BOUNDARIES.md` and SecureRails boundary docs.
- **What not to do:** do not weaken boundary statements.

## Claim-audit false positive
- **Symptom:** claim checker flags a negative boundary statement.
- **Likely cause:** ambiguous sentence structure.
- **Fix:** make negation explicit (e.g., “is not a certification claim”).
- **What not to do:** do not remove boundary text entirely.

## Missing safety ledger counter
- **Symptom:** run passes partially but evidence package is incomplete.
- **Likely cause:** safety ledger generation omitted field(s).
- **Fix:** populate required counters and validate schema/tests.
- **What not to do:** do not publish partial dockets.

## Broken link
- **Symptom:** link audits fail.
- **Likely cause:** renamed/moved documentation file.
- **Fix:** update references in README/docs and rerun audits.
- **What not to do:** do not leave stale links for later.

## Workflow artifact not found
- **Symptom:** replay or review job cannot find required artifact.
- **Likely cause:** artifact upload step name/path mismatch.
- **Fix:** align upload/download names and verify manifest paths.
- **What not to do:** do not bypass replay requirements.

## Pages did not update
- **Symptom:** GitHub Pages content stays stale.
- **Likely cause:** `evidence-hub-publish` failed or lacked permissions.
- **Fix:** inspect publish logs, fix root cause, rerun publisher.
- **What not to do:** do not add direct Pages deploy in random workflow.

## Evidence Mission Control did not publish
- **Symptom:** new run not visible in mission control page.
- **Likely cause:** index build or publish stage failed.
- **Fix:** check `evidence-hub-publish.yml` + repair/canary workflows.
- **What not to do:** do not manually edit generated run records without provenance.

## Replay failed
- **Symptom:** independent replay mismatch or non-deterministic output.
- **Likely cause:** missing seed/config/environment drift.
- **Fix:** use recorded inputs/seed, verify manifest hash and dependencies.
- **What not to do:** do not claim reproducibility until replay passes.

## Falsification failed
- **Symptom:** falsification audit rejects run claims.
- **Likely cause:** claim too strong for evidence tier.
- **Fix:** downgrade claim level or improve evidence quality.
- **What not to do:** do not relabel failed falsification as pass.

## no-auto-merge check failed
- **Symptom:** safe PR cannot auto-merge.
- **Likely cause:** guardrail intentionally blocks autonomous merge.
- **Fix:** require human review and approval path.
- **What not to do:** do not force merge without policy sign-off.

## use-case triage failed
- **Symptom:** workflow blocked by governance triage.
- **Likely cause:** ambiguous use-case classification.
- **Fix:** refine use-case description and boundary tags.
- **What not to do:** do not reclassify high-risk tasks as low-risk to pass.

## GitHub Actions permission warning
- **Symptom:** warning about excessive or missing permissions.
- **Likely cause:** workflow permissions are too broad or too narrow.
- **Fix:** set least-privilege permissions explicitly.
- **What not to do:** do not grant write-all by default.

## Node.js action deprecation warning
- **Symptom:** actions runtime deprecation notices.
- **Likely cause:** outdated action versions.
- **Fix:** bump actions to maintained releases and retest.
- **What not to do:** do not ignore repeated deprecation warnings.

## SecureRails Agentic PR Guard 001
- Ensure `python -m secure_rails_pr_guard analyze` and `validate` pass locally.

## SecureRails installable action / reusable workflow
- Confirm caller workflow uses read-only permissions and does not use `pull_request_target`.
- Confirm production callers pin to release tag or commit SHA (not `main`).
- Review `securerails-pr-guard-output/summary.md` and Evidence Docket before any remediation decision.

- Check webhook signature using `python -m secure_rails github-app verify-webhook ...`


- SecureRails E2E Pilot Canary 001: synthetic internal canary workflow.

## SecureRails Trust Center troubleshooting
- security.txt missing contact: keep template-only/pending_contact until real security contact is configured.
- trust-center check failure: run `python scripts/secure_rails_trust_center_check.py .`.
- incident schema failure: validate `docs/secure-rails/templates/security-incident-record-example.json`.
- certification overclaim failure: remove prohibited certification/guarantee/exemption claims.

## Recursive Gauntlet
If validate fails, ensure lock-candidates runs before generate-heldout.
