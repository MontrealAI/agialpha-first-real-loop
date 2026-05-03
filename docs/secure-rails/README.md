# SecureRails User Guide

SecureRails is AGI ALPHA’s AI-agent security governance and proof-bound defensive remediation layer.

It secures the rails for autonomous software work by converting agent actions, workflow changes, findings, and remediation proposals into replayable ProofBundles, Evidence Dockets, redacted safety ledgers, safe PR proposals, validator reports, and reusable defensive capability.

SecureRails makes AI-agent work:

```text
safe to review
safe to replay
safe to reject
safe to remediate
safe to archive
safe to govern
```

## One-sentence positioning

SecureRails is AI-agent security governance and proof-bound defensive remediation.

## What SecureRails is

SecureRails is:

* AI-agent security governance
* proof-bound defensive remediation
* repo-owned defensive evidence infrastructure
* human-reviewed remediation support
* claim-boundary enforcement
* compliance-as-code for agentic software work
* a ProofBundle and Evidence Docket production layer
* a safety ledger and validation layer
* a reusable defensive capability archive

## What SecureRails is not

SecureRails is not:

* autonomous cybersecurity assurance or attestation
* offensive cybersecurity tooling
* external target scanning
* exploit execution
* malware generation
* social engineering
* a high-risk AI system by intended purpose
* an autonomous decision-making system
* a GPAI model provider by default
* designed for HR or worker evaluation
* designed for profiling natural persons
* designed for automated decisions about natural persons
* designed as a safety component of critical infrastructure
* an investment product

All SecureRails outputs are advisory and require independent human validation before action.

## The SecureRails loop

```text
Agentic work event
→ ProofBundle
→ Evidence Docket
→ validator report
→ redacted safety ledger
→ safe remediation / rejection / escalation
→ reusable defensive capability
→ vNext defensive task
```

The operating doctrine:

> No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## What problem SecureRails solves

AI agents can generate code, PRs, workflow changes, configuration changes, and remediation proposals faster than humans can safely review them.

SecureRails creates a governance layer around that work. It does not merely detect risk. It makes the work reviewable, replayable, rejectable, remediable, and auditable.

## Who this is for

SecureRails is for:

* AI-agent operators
* engineering teams using autonomous or semi-autonomous coding agents
* security reviewers
* platform teams
* DevSecOps teams
* compliance reviewers
* AI governance teams
* AGI ALPHA Evidence Mission Control operators

## What SecureRails reviews

SecureRails can review repo-owned, defensive software-work artifacts such as:

* pull requests
* workflow changes
* GitHub Actions permissions
* Evidence Docket completeness
* ProofBundle integrity
* safety ledgers
* claim boundaries
* redacted secret-hygiene reports
* safe remediation proposals
* documentation and public claims
* deployment intake records
* AI Act use-case triage records

## Allowed use

SecureRails is intended for:

* repo-owned defensive review
* AI-agent work governance
* proof-bound remediation
* claim-boundary enforcement
* workflow safety review
* redacted safety-ledger production
* safe PR proposal review
* human-governed remediation
* Evidence Docket and ProofBundle production

## Excluded use

SecureRails must not be used for:

* employment evaluation
* worker management
* profiling of natural persons
* automated decisions about natural persons
* law-enforcement decisioning
* biometric identification
* emotion recognition
* credit, insurance, education, medical, or migration decisions
* critical-infrastructure safety-component reliance
* offensive cybersecurity
* external target scanning
* exploit execution
* malware generation
* social engineering
* autonomous production remediation
* autonomous merge
* cybersecurity assurance or attestation claims
* guaranteed security claims
* investment or token-return claims

## EU AI Act posture

SecureRails is designed and documented as a defensive governance and evidence system for software work.

SecureRails is not intended, designed, validated, or authorized for Annex III high-risk AI use cases.

SecureRails analyzes:

```text
code
workflows
pull requests
artifacts
claims
Evidence Dockets
ProofBundles
safety ledgers
validator reports
```

SecureRails does not evaluate people.

Every deployment should include:

* deployment intake
* customer use attestation
* excluded-use review
* Annex III triage
* human-review policy
* material modification log
* safety ledger
* claim-boundary review

## Important boundary

Do not say:

```text
SecureRails is EU AI Act exempt.
SecureRails is legally approved worldwide.
SecureRails provides formal security attestation.
SecureRails guarantees security.
SecureRails autonomously remediates production systems.
```

Use this instead:

```text
SecureRails is designed as AI-agent security governance and proof-bound defensive remediation, with human-reviewed promotion, excluded high-risk uses, and executable guardrails.
```

## Key files

### Public docs

* [Product boundary](product-boundary.md)
* [EU AI Act positioning](eu-ai-act-positioning.md)
* [Foreseeable misuse and excluded uses](foreseeable-misuse-and-excluded-uses.md)
* [Security and safety boundary](security-safety-boundary.md)
* [Claims and marketing guardrails](claims-and-marketing-guardrails.md)
* [Work Vaults, MARK, and Sovereigns](work-vaults-mark-sovereigns.md)
* [SecureRails index](index.md)

### Templates

* [Templates README](templates/README.md)
* [Deployment intake example](templates/deployment-intake-example.json)
* [Safety ledger example](templates/safety-ledger-example.json)

### Guard scripts

From the repository root:

```text
scripts/secure_rails_claim_boundary_check.py
scripts/secure_rails_safety_ledger_check.py
scripts/secure_rails_no_automerge_check.py
scripts/secure_rails_use_case_triage_check.py
```

### Workflow

```text
.github/workflows/secure-rails-compliance-guard.yml
```

## How to run the checks locally

From the repository root:

```bash
python scripts/secure_rails_claim_boundary_check.py .
python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json
python scripts/secure_rails_no_automerge_check.py .
python scripts/secure_rails_use_case_triage_check.py docs/secure-rails/templates/deployment-intake-example.json
```

## What the compliance guard enforces

The SecureRails compliance guard checks that the repository does not drift into unsafe or overbroad claims.

It enforces:

* no AGI / ASI overclaims
* no empirical SOTA claims without evidence
* no cybersecurity assurance or attestation claims
* no guaranteed security claims
* no offensive cyber posture
* no autonomous decision-making posture
* no HR / worker-evaluation posture
* no profiling posture
* no critical-infrastructure safety-component reliance
* no GPAI model-provider claim by default
* no investment-product framing
* no auto-merge posture
* safety ledger hard counters

## Hard safety counters

Security-related SecureRails reports should include these counters:

```text
raw_secret_leak_count
external_target_scan_count
exploit_execution_count
malware_generation_count
social_engineering_content_count
unsafe_automerge_count
critical_safety_incidents
```

For promotion, all hard safety counters must be explicitly zero.

## How to use SecureRails for a new deployment

1. Complete deployment intake.
2. Confirm excluded uses.
3. Run AI Act triage.
4. Generate or attach the Evidence Docket.
5. Run the SecureRails compliance guard.
6. Review the safety ledger.
7. Review any safe PR proposal manually.
8. Record the human-review decision.
9. Archive accepted defensive capability.
10. Re-screen after any material modification.

## Human review is mandatory

SecureRails may produce:

* evidence
* validator reports
* safety ledgers
* safe PR proposals
* rejection dockets
* remediation recommendations

SecureRails must not automatically merge or autonomously promote remediation.

## Marketing rule

Approved:

```text
SecureRails makes AI-agent work safe to review, safe to replay, and safe to remediate.
```

Avoid:

```text
SecureRails guarantees security.
SecureRails certifies compliance.
SecureRails is fully EU AI Act exempt.
SecureRails autonomously remediates production systems.
```

## $AGIALPHA boundary

If $AGIALPHA is referenced, it must be framed only as utility infrastructure for protocol operations such as:

* access credits
* escrow
* validator staking
* Sybil resistance
* validator fees
* replay fees
* slashing
* ProofBundle fees
* Evidence Docket fees
* α-Work Unit accounting
* settlement receipts
* archive-access accounting

Do not describe $AGIALPHA as:

* equity
* debt
* yield
* dividend
* ownership
* profit rights
* investment return
* guaranteed appreciation
* financial product

## Current status

SecureRails has repository-level compliance-as-code enforcement through:

```text
.github/workflows/secure-rails-compliance-guard.yml
```

This is an enforcement layer, not a certification claim.

## Final boundary

SecureRails is AI-agent security governance and proof-bound defensive remediation. It is not autonomous cybersecurity assurance or attestation, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.
