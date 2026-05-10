# SecureRails Templates

These templates are governance evidence scaffolds. They support bounded defensive review and must not be used for overclaiming.

## Template catalog
- `deployment-intake-example.json`
  - What: customer/repo deployment intake.
  - When: before pilot/deployment review.
  - Validate: `python scripts/secure_rails_use_case_triage_check.py docs/secure-rails/templates/deployment-intake-example.json`
  - Must not change: top-level required keys and excluded-use declarations.
  - Boundary: intake is not legal approval or certification.

- `safety-ledger-example.json`
  - What: hard safety counters and review controls.
  - When: every governed deployment/evidence package.
  - Validate: `python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json`
  - Must not change: required counter names/semantics.
  - Boundary: safety ledger is governance evidence, not guaranteed security.

- `work-vault-example.json`
- `mark-allocation-example.json`
- `sovereign-example.json`
- `vault-settlement-example.json`
  - What: Work Vault / MARK / Sovereign / settlement lifecycle examples.
  - When: recording utility-accounting lifecycle events.
  - Validate: `python scripts/secure_rails_work_vault_check.py <template-path>`
  - Must not change: schema-critical IDs, lifecycle fields, and evidence linkage.
  - Boundary: utility accounting only; not investment framing.

- `customer-use-attestation.md` (if present)
- `annex-iii-triage-record.md` (if present)
- `material-modification-log.md` (if present)
  - What: human attestations and change governance records.
  - When: deployment readiness and post-change re-screening.
  - Boundary: reviewer records support compliance posture, not legal guarantees.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.


## Registry examples
- Work Vault example: `work-vault-example.json`
- MARK allocation example: `mark-allocation-example.json`
- Sovereign example: `sovereign-example.json`
- Settlement example: `vault-settlement-example.json`

- PR Guard manifest template: [pr-guard-example-manifest.json](pr-guard-example-manifest.json)
- PR Guard report template: [pr-guard-example-report.json](pr-guard-example-report.json)

- artifact-manifest-example.json
- provenance-record-example.json
- repository-health-example.json

- customer-securerails-pr-guard.yml
  - Copy-paste external repository workflow caller for SecureRails PR Guard reusable workflow.
  - For production, pin workflow reference to release tag or commit SHA, not main.

- customer-pilot-intake-example.json
- external-repo-record-example.json
- repository-dispatch-payload-example.json

- Added connector templates: customer-installation and dispatch bridge.

- `instance-config-example.json`: SecureRails Template Bootstrap example instance configuration.


## SecureRails E2E Pilot Canary 001
See `docs/secure-rails/e2e-pilot-canary.md` and workflow `.github/workflows/securerails-e2e-pilot-canary-001.yml`.
