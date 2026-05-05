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
