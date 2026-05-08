# SecureRails Customer Pilot Installation

1. Copy `docs/secure-rails/templates/customer-securerails-pr-guard.yml` into your repo `.github/workflows/`.
2. Open a pull request.
3. Wait for **SecureRails Agentic PR Guard** check to finish.
4. Download the `securerails-pr-guard-output` artifact.
5. Review `summary.md` and the Evidence Docket.
6. Decide: accept, reject, or escalate for remediation.

Human review is required. SecureRails outputs are advisory artifacts.

For production, replace `@main` with a release tag or commit SHA.

SecureRails is AI-agent security governance and proof-bound defensive remediation. It is not autonomous cybersecurity-certification, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.
