# Promotion Gates

SecureRails Human Review Console 001 enforces **No human decision record, no promotion**.

## Promotion targets

- `safe_pr`
- `capability_archive`
- `release`
- `policy_update`
- `customer_pilot_status`

## Required conditions

Promotion-gate records require:

- human review decision present
- Evidence Docket present (when required for target)
- ProofBundle present
- safety ledger present
- claim boundary present
- hard safety counters zero
- auto-merge disallowed

If any required condition fails, the gate status is `fail` and promotion must not proceed.

## Operational boundary

Passing a promotion gate is governance readiness evidence only. It is not security certification and does not permit automatic merge.

Manual merge required. No auto-merge.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
