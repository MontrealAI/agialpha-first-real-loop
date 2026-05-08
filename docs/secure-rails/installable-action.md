# SecureRails Installable Action

The SecureRails installable action (`.github/actions/securerails-pr-guard`) runs defensive, data-only SecureRails checks and writes advisory outputs to an output directory.

## Outputs
- summary
- Evidence Docket folder
- Work Vault file
- safety ledger file
- run manifest
- recommendation

## Modes
`pr_guard`, `compliance_guard`, `work_vault`, `supply_chain`.

## Safety defaults
- read-only workflow permissions
- no secrets required
- no auto-merge
- no untrusted PR code execution
- no offensive cyber behavior

## Usage
- In this repo: use `.github/workflows/securerails-pr-guard-demo.yml`.
- External repos: call the reusable workflow.

For production, pin to a release tag or commit SHA, not `main`.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
