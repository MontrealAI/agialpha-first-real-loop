# SecureRails Installable Action

The installable action (`.github/actions/securerails-pr-guard`) runs SecureRails defensive checks and produces advisory artifacts (summary, Evidence Docket path, Work Vault path, safety-ledger path, evidence manifest path, recommendation).

## Modes
`pr_guard`, `compliance_guard`, `work_vault`, `supply_chain`.

## Permissions and safety defaults
- Read-only workflow permissions.
- No secrets required.
- No `pull_request_target`.
- No auto-merge.
- No untrusted PR code execution.
- Human review required.

## Using in this repo
Use `.github/workflows/securerails-pr-guard-demo.yml` or `securerails-pr-guard-reusable.yml`.

## Using in external repos
Call the reusable workflow from `MontrealAI/agialpha-first-real-loop` and pin to a release tag or commit SHA for production.

## Artifacts and interpretation
Download the `securerails-pr-guard-output` artifact and review `summary.md`, Evidence Docket files, and recommendation as advisory only.

## Claim boundary
No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
SecureRails is AI-agent security governance and proof-bound defensive remediation, not autonomous cybersecurity-certification, not offensive cyber, and not an investment product.

## Troubleshooting
Run local checks in README and verify docs/workflow audits before release.
