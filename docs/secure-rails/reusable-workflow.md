# SecureRails Reusable Workflow

Workflow: `.github/workflows/securerails-pr-guard-reusable.yml`.

It exposes `workflow_call` inputs for mode, strictness, Evidence Docket generation, Work Vault generation, settlement record generation, token utility mode, and artifact upload.

## Security model
- permissions are read-only (`contents`, `pull-requests`, `actions`)
- no write permissions
- no secrets required
- no `pull_request_target`
- no auto-merge
- human review required

## Caller example
See `docs/secure-rails/templates/customer-securerails-pr-guard.yml`.

For production, pin to `@v1` or `@<commit-sha>`; `@main` is for demos only.
