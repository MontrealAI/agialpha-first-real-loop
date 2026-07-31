# Decision Ledger

SecureRails Human Review Console 001 enforces **No human decision record, no promotion**.

## Ledger purpose

The Decision Ledger is a durable, auditable registry for human-review requests, decisions, and promotion-gate outcomes.

## Structure

Registry path: `secure_rails_reviews/`

- `registry.json`: full history record set
- `latest.json`: latest pointers and summary values
- `requests/`: review-request records
- `decisions/`: reviewer decisions
- `promotion_gates/`: promotion-gate records
- `indexes/`: lookup indexes (status, decision, reviewer, Work Vault, Evidence Docket, policy decision)

## History preservation and supersession

The ledger preserves prior records and may mark older decisions as `superseded` when a newer decision replaces them. Superseded records remain auditable and are not silently deleted.

Supported ledger statuses:

- `pending`
- `accepted`
- `rejected`
- `escalated`
- `request_changes`
- `archive_only`
- `superseded`
- `invalid`
- `incomplete`

## Private/customer-redacted support

Records may be redacted for customer confidentiality while retaining required governance metadata (IDs, timestamps, reviewer role, safety counters, gate result, and claim boundary).

## Validation

- `python -m secure_rails human-review validate-ledger --registry secure_rails_reviews`
- `python -m secure_rails human-review build-data --registry secure_rails_reviews --out docs/_generated/secure-rails/human-review`

Manual merge required. No auto-merge.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
