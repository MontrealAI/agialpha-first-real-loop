# SecureRails Work Vaults, ALPHA AGI MARK, and ALPHA AGI Sovereigns

SecureRails Work Vaults are the protocol boundary that converts AI-agent defensive work into auditable, human-governed remediation decisions.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## Scope and boundary

SecureRails is AI-agent security governance and proof-bound defensive remediation. It is not autonomous cybersecurity assurance or attestation, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.

All outputs are advisory and require independent human validation before action.

$AGIALPHA in this protocol is utility infrastructure for protocol operations only. It is not investment, equity, yield, dividend, appreciation, ownership, or a financial product claim.

## Lifecycle

```text
SecureRails Work Vault
→ ALPHA AGI MARK allocation
→ ALPHA AGI Sovereign assignment
→ AGI Job execution
→ ProofBundle production
→ Evidence Docket assembly
→ Human review decision
→ Safe remediation / rejection / escalation
→ $AGIALPHA utility settlement receipt
→ Reusable defensive capability archive
→ vNext defensive work
```

## Core entities

- **Work Vault**: isolated, deterministic job context with pinned inputs, policy controls, and immutable run IDs.
- **ALPHA AGI MARK allocation**: governance allocation record that authorizes a bounded defensive job under explicit replay/validator requirements.
- **ALPHA AGI Sovereign assignment**: assignment of accountable defensive operating policy and reviewers to a vault run.
- **AGI Job**: deterministic task run that emits artifacts and logs.
- **ProofBundle**: reproducible evidence package (inputs, outputs, checksums, commands).
- **Evidence Docket**: claim-bound, reviewer-readable evidence summary and decision record.
- **Settlement receipt**: protocol utility accounting receipt for operations tracking only (no real transfer).

## Deterministic execution requirements

1. Stable job ID derived from normalized JSON inputs.
2. Stable ordering for all list/object serialization.
3. No network or external target scanning required for pipeline validation.
4. Replay output must hash-identical for identical input.
5. Human review gates must remain explicit before promotion.

## Safety requirements

- Defensive-only remediation recommendations.
- No exploit execution, malware creation, secret disclosure, or social engineering.
- No autonomous merge.
- No autonomous claim promotion.
- Reject if Evidence Docket is missing or incomplete.

## Evidence Mission Control integration

Mission Control operators should register each Work Vault run using generated run IDs and docket IDs, then link the docket and ProofBundle in evidence index pages.

Suggested integration fields:

- `work_vault.vault_id`
- `mark_allocation.mark_id`
- `sovereign_assignment.sovereign_id`
- `proof_bundle.proof_bundle_id`
- `evidence_docket.docket_id`
- `human_review.decision`
- `utility_settlement.receipt_id`

## Reference artifacts

- `schemas/secure_rails_work_vault_record.schema.json`
- `schemas/secure_rails_work_vault_request.schema.json`
- `sample_outputs/secure_rails_work_vault/sample_input.json`
- `sample_outputs/secure_rails_work_vault/sample_work_vault_run.json`
- `scripts/secure_rails_work_vault_pipeline.py`
- `tests/test_secure_rails_work_vault_pipeline.py`
