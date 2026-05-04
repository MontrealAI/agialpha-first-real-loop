# SecureRails Templates README

For each template: use only as example input, keep schema keys stable, validate before use, and keep claims bounded.

- `deployment-intake-example.json`: customer/repo use-case intake. Validate with `python scripts/secure_rails_use_case_triage_check.py docs/secure-rails/templates/deployment-intake-example.json`.
- `safety-ledger-example.json`: hard safety counters. Validate with `python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json`.
- `work-vault-example.json`: Work Vault record. Validate with `python scripts/secure_rails_work_vault_check.py docs/secure-rails/templates/work-vault-example.json`.
- `mark-allocation-example.json`: MARK allocation record. Validate with `python scripts/secure_rails_work_vault_check.py docs/secure-rails/templates/mark-allocation-example.json`.
- `sovereign-example.json`: Sovereign assignment record. Validate with `python scripts/secure_rails_work_vault_check.py docs/secure-rails/templates/sovereign-example.json`.
- `vault-settlement-example.json`: utility settlement record. Validate with `python scripts/secure_rails_work_vault_check.py docs/secure-rails/templates/vault-settlement-example.json`.

If present, include `customer-use-attestation.md`, `annex-iii-triage-record.md`, `material-modification-log.md` in your Evidence Docket package.

Claim boundary: templates support governance evidence only; they are not certification, legal approval, investment framing, or autonomous claim promotion.
