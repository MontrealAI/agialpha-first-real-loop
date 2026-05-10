# Customer Install Bundle
SecureRails is AI-agent security governance and proof-bound defensive remediation.
It is not autonomous cybersecurity assurance, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.

For production pilots, pin to a release tag or commit SHA. Do not rely on main.

```yaml
name: SecureRails Agentic PR Guard
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  workflow_dispatch:
permissions:
  contents: read
  pull-requests: read
  actions: read
jobs:
  securerails:
    uses: MontrealAI/agialpha-first-real-loop/.github/workflows/securerails-pr-guard-reusable.yml@v0.1.0
    with:
      mode: pr_guard
      strict: true
      generate_evidence_docket: true
      generate_work_vault: true
      generate_settlement_record: true
      token_utility_mode: mock
      upload_artifact: true
```
