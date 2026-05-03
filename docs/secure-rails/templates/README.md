# SecureRails Templates

This folder contains example inputs used by the SecureRails compliance guard and deployment workflow.

These templates help operators keep SecureRails deployments inside the intended product boundary:

```text
AI-agent security governance
proof-bound defensive remediation
human-reviewed promotion
no autonomous claim escalation
```

## Current templates

### `deployment-intake-example.json`

A low-risk deployment intake example.

It should confirm that the deployment is:

* repo-owned
* defensive
* human-reviewed
* not used for HR or worker evaluation
* not used for profiling natural persons
* not used for automated decisions about natural persons
* not used as a critical-infrastructure safety component
* not offensive cyber
* not a GPAI model-provider deployment by default

Use this template to test:

```bash
python scripts/secure_rails_use_case_triage_check.py docs/secure-rails/templates/deployment-intake-example.json
```

### `safety-ledger-example.json`

A minimal safety ledger example.

It should include these hard safety counters, all explicitly set to `0`:

```text
raw_secret_leak_count
external_target_scan_count
exploit_execution_count
malware_generation_count
social_engineering_content_count
unsafe_automerge_count
critical_safety_incidents
```

Use this template to test:

```bash
python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json
```

## How to use these templates

For a new SecureRails deployment:

1. Copy `deployment-intake-example.json`.
2. Rename it for the customer, repo, or deployment.
3. Fill in the actual deployment scope.
4. Confirm excluded uses.
5. Run use-case triage.
6. Copy `safety-ledger-example.json`.
7. Fill in the actual safety counters.
8. Run the safety ledger check.
9. Attach both files to the Evidence Docket.

## Required deployment posture

A valid SecureRails deployment should remain:

* defensive
* repo-owned
* human-reviewed
* advisory
* evidence-producing
* claim-bounded
* safety-ledgered

## Excluded deployment posture

A SecureRails deployment is not valid if it is used for:

* employment evaluation
* worker management
* profiling of natural persons
* automated decisions about natural persons
* biometric identification
* emotion recognition
* law-enforcement decisioning
* credit or insurance decisions
* education access decisions
* medical triage or diagnosis
* migration or asylum decisions
* critical-infrastructure safety-control reliance
* offensive cybersecurity
* external target scanning
* exploit execution
* malware generation
* social engineering
* autonomous production remediation
* autonomous merge

## Human review requirement

SecureRails outputs are advisory and require independent human validation before any action.

A safe PR proposal is not a merge authorization.

An Evidence Docket is not a security assurance or attestation.

A passed compliance guard is not legal approval.

## Claim boundary

Use this boundary in deployment records:

```text
SecureRails is AI-agent security governance and proof-bound defensive remediation. It is not autonomous cybersecurity assurance or attestation, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.
```

## Local checks

From the repository root, run:

```bash
python scripts/secure_rails_claim_boundary_check.py .
python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json
python scripts/secure_rails_no_automerge_check.py .
python scripts/secure_rails_use_case_triage_check.py docs/secure-rails/templates/deployment-intake-example.json
```

## SecureRails doctrine

> No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
