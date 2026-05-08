# Customer Pilot Installation

1. Copy `docs/secure-rails/templates/customer-securerails-pr-guard.yml` into `.github/workflows/` of your repository.
2. Open a PR or run manually with `workflow_dispatch`.
3. Review workflow checks and download `securerails-pr-guard-output`.
4. Read `summary.md` and Evidence Docket files.
5. Decide: accept, reject, or escalate to SecureRails operator.

Use read-only permissions and no secrets. Do not enable auto-merge.

For production, pin to a release tag or commit SHA (not `main`).

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
Human review is required for remediation decisions.
