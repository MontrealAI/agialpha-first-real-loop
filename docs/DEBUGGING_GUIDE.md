# Debugging Guide

Do not fix by disabling the test.

## Common failures and fixes
- Missing script in workflow: verify script path in `scripts/` and workflow `run` step.
- Workflow not documented: add `.yml` file name to `docs/WORKFLOW_CATALOG.md`.
- Claim audit false positive: adjust wording to bounded-evidence phrasing.
- Link audit failure: fix relative links and target filenames.
- README audit failure: keep launchpad concise and include required boundary text.
- Evidence Mission Control build failure: inspect publisher workflow + generated artifacts.
- SecureRails Compliance Guard failure: run each guard script locally and fix failing input.
- Safety ledger missing counter: update ledger template/instance with required counters.
- Use-case triage failure: complete required intake fields and excluded-use decisions.
- No-auto-merge failure: remove/disable auto-merge behavior in workflow or policy.
- Workflow catalog stale: sync `docs/WORKFLOW_CATALOG.md` with `.github/workflows/*`.
- Artifact missing/expired: rerun workflow and archive outputs promptly.
- GitHub Pages not updating: verify only central publisher deploys Pages.

## Fast command set
```bash
python -m unittest discover -s tests
python -m agialpha_docs audit-workflows --repo-root .
python -m agialpha_docs audit-claims --repo-root .
python -m agialpha_docs audit-links --repo-root .
python -m agialpha_docs audit-readmes --repo-root .
python scripts/secure_rails_claim_boundary_check.py .
python scripts/secure_rails_no_automerge_check.py .
```
