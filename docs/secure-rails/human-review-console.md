# Human Review Console

SecureRails Human Review Console 001 is the human-governed promotion layer that records explicit reviewer outcomes for SecureRails artifacts.

## Why it exists

The console exists to enforce this operational rule:

**No human decision record, no promotion.**

SecureRails chain:

Work Vault → MARK allocation → Sovereign assignment → ProofBundle → Evidence Docket → Policy Kernel decision → Human Review Console → Decision Ledger → safe remediation / rejection / escalation / archive-only → $AGIALPHA utility settlement record → Capability Archive → Evidence Mission Control visibility.

## Allowed review decisions

- `accept`
- `reject`
- `escalate`
- `request_changes`
- `archive_only`
- `pending` (ledger status while waiting for reviewer input)

An `accept` decision means a reviewer accepted the evidence outcome under stated conditions. It does not authorize auto-merge.

## Requesting a review

1. Submit a SecureRails human-review request issue via `.github/ISSUE_TEMPLATE/securerails-human-review.yml`.
2. Include source references (for example Work Vault ID, Evidence Docket ID, ProofBundle ID, policy decision ID, PR URL, artifact URL).
3. State requested decision and risk tier.
4. Confirm claim-boundary preservation and human-review requirement.

## Recording a decision

1. Create a decision record using the human-review decision schema.
2. Validate with `python -m secure_rails human-review validate-decision --input <decision.json>`.
3. Update the ledger with `python -m secure_rails human-review update-ledger --input <decision.json> --registry secure_rails_reviews`.
4. Validate ledger integrity with `python -m secure_rails human-review validate-ledger --registry secure_rails_reviews`.

## Promotion requirements

Promotion gates require human decision, Evidence Docket, ProofBundle, safety ledger checks, claim-boundary checks, and hard safety counters at zero.

Manual merge required. No auto-merge.

## Evidence Mission Control visibility

Generated JSON in `docs/_generated/secure-rails/human-review/` provides:

- request and decision lists
- gate outcomes
- summary counters for pending, accepted, rejected, escalated, request changes, and archive-only decisions

## Claim boundary and non-claims

SecureRails is AI-agent security governance and proof-bound defensive remediation. It is not autonomous cybersecurity certification, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
