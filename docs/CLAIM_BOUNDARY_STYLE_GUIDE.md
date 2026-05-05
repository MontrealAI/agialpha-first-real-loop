# Claim Boundary Style Guide

## Doctrine
No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## Allowed language
Use wording that stays inside current evidence scope:
- bounded local evidence
- proof-bound defensive remediation
- human-reviewed promotion
- utility infrastructure
- replayable Evidence Dockets
- safe PR proposals
- defensive repo-owned review
- local/proxy CI evidence

## Forbidden language
Do not use language that implies unsupported capability, legal sign-off, or financial entitlement:
- unsupported frontier-intelligence attainment claims
- unsupported top-performance claims without benchmark+docket+independent replay
- security-assurance certification claims
- guaranteed security
- safe autonomy
- autonomous production remediation
- benchmark-victory statements without evidence chain
- EU AI Act exempt
- legally approved worldwide
- guaranteed economic-outcome language
- investment product
- token appreciation / yield / dividend / ownership rights / profit rights

## Good vs bad phrasing
| Good (safe) | Bad (forbidden) | Why |
|---|---|---|
| "This run produced bounded CI evidence and replay artifacts." | "This proves frontier intelligence." | CI evidence is local/proxy evidence, not AGI proof. |
| "SecureRails proposes defensive remediation for human review." | "SecureRails autonomously secures production." | Human decision and bounded scope are mandatory. |
| "Benchmark status is pending independent replay." | "We are best overall." | SOTA claims need benchmark execution + replay + attestation. |
| "$AGIALPHA records utility accounting events." | "$AGIALPHA provides investment return." | Utility accounting is allowed; investment framing is forbidden. |

## What to do next
Before merging docs, run:
```bash
python -m agialpha_docs audit-claims --repo-root .
python scripts/secure_rails_claim_boundary_check.py .
```
