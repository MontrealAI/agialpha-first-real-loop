# SecureRails Work Vaults, MARK, and Sovereigns

SecureRails is AI-agent security governance and proof-bound defensive remediation.

It does not provide autonomous certification of cybersecurity outcomes, not offensive cyber tooling, not a high-risk AI decision system by intended purpose, not a GPAI model provider by default, and not a speculative monetary instrument.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## Canonical protocol chain

AI-agent work event
→ SecureRails Work Vault
→ ALPHA AGI MARK allocation
→ ALPHA AGI Sovereign assignment
→ AGI Job execution
→ ProofBundle
→ Evidence Docket
→ validator decision
→ human review
→ safe remediation / rejection / escalation
→ $AGIALPHA utility settlement
→ CyberSecurityCapabilityArchive
→ vNext defensive work

## What is a SecureRails Work Vault?

A SecureRails Work Vault is a bounded protocol container for one unit of AI-agent defensive work. It records scope, required validators, safety counters, proof requirements, evidence requirements, human-review gates, and utility settlement records.

A Work Vault is not an economic instrument and does not represent transferable value rights.

### Lifecycle

`proposed → MARK_scored → vault_opened → sovereign_assigned → job_started → proof_submitted → validator_review → evidence_docket_created → human_review → accepted/rejected/escalated → settled → archived → vNext_reuse_tested`

### Hard rules

- no vault, no settlement
- no ProofBundle, no Evidence Docket
- no Evidence Docket, no strong claim
- no human review, no promotion
- no auto-merge
- no offensive cyber, external target scanning, exploit execution, malware generation, or social engineering
- no HR/worker evaluation, profiling of natural persons, or automated decisions about natural persons
- no critical-infrastructure safety-component reliance
- no speculative token framing

## ALPHA AGI MARK (allocation kernel)

MARK allocates bounded protocol capacity: risk tier, review priority, validator coverage, and utility budget proxy.

MARK does not allocate market capital and does not target monetary upside. MARK outputs are advisory governance allocations that must still pass validation and human review.

### MARK hard gates

- repo-owned and defensive-only scope
- proof required + replay required + falsification required
- human review required
- auto-merge disabled
- promotion without evidence disabled

## ALPHA AGI Sovereigns

A Sovereign is a bounded, specialized, proof-producing work organ for a task family (for example workflow permissions, secret hygiene, claim boundary assurance, or Evidence Docket integrity).

A Sovereign is not a legal sovereign, regulator, certifier, or monopoly authority.

Each Sovereign defines:
- allowed and forbidden work classes
- validator set
- ProofBundle policy
- Evidence Docket policy
- promotion policy with human-review gate

## $AGIALPHA utility accounting boundary

$AGIALPHA is utility infrastructure for protocol operations only:
- utility budget
- validator/replay/proof/evidence fees
- α-Work Unit accounting
- settlement receipt records
- bounded-work escrow and archive-reuse accounting

It is not a rights-bearing monetary instrument and does not imply upside guarantees or payout rights.

## Settlement and slashing semantics

Settlement is a **utility settlement record** tied to validated protocol work. It is not an market-linked return.

Honest failure is not slashable. Slashing is limited to defined misconduct (for example fabricated artifacts, false replay success, raw secret leakage, prohibited scanning/exploit behavior, unsafe auto-merge, falsified Evidence Docket hash, or deliberate claim-boundary removal).

## JSON references

- Work Vault schema: `schemas/securerails_work_vault.schema.json`
- MARK allocation schema: `schemas/securerails_mark_allocation.schema.json`
- Sovereign schema: `schemas/securerails_sovereign.schema.json`
- Vault settlement schema: `schemas/securerails_vault_settlement.schema.json`

Templates:
- `docs/secure-rails/templates/work-vault-example.json`
- `docs/secure-rails/templates/mark-allocation-example.json`
- `docs/secure-rails/templates/sovereign-example.json`
- `docs/secure-rails/templates/vault-settlement-example.json`

Validation command:

```bash
python scripts/secure_rails_work_vault_check.py docs/secure-rails/templates/work-vault-example.json
```

## Evidence Mission Control recommendation

On SecureRails pages, display the canonical protocol chain and link to this document. Keep claim boundaries visible near any Work Vault, MARK, Sovereign, ProofBundle, Evidence Docket, or settlement summary.

## Final boundary

SecureRails outputs are advisory and promotion-gated by validators plus human review. SecureRails is not intended, designed, validated, or authorized for Annex III high-risk AI use cases.
