# SecureRails Security and Safety Boundary

## Allowed

- Repo-owned defensive review.
- Local workflow permission review.
- Local Evidence Hub repair.
- Local secret-like pattern detection with strict redaction.
- Artifact integrity checks.
- ProofBundle and Evidence Docket checks.
- Safe PR proposals.
- External reviewer kit generation.
- Delayed-outcome sentinels.
- Human-reviewed remediation.

## Forbidden

- External target scanning.
- Exploit execution.
- Credential collection.
- Malware generation.
- Social engineering.
- Automatic merge.
- Uncontrolled external actuation.
- Printing secret values.
- Real-world security certification claims.
- Offensive capability claims.
- Empirical SOTA claims without official benchmark evidence and independent replay.
- Guaranteed security or guaranteed commercial outcome.

## Hard safety invariants

```json
{
  "raw_secret_leak_count": 0,
  "external_target_scan_count": 0,
  "exploit_execution_count": 0,
  "malware_generation_count": 0,
  "social_engineering_content_count": 0,
  "unsafe_automerge_count": 0,
  "critical_safety_incidents": 0
}
```

If any hard safety invariant is nonzero, the run fails promotion.

## Redaction rule

Never print raw secret-like values. Reports may include file path, line number, finding type, and salted hash only.

## Artifact rule

Do not execute downloaded artifacts. Parse artifacts only as data and escape artifact-derived HTML.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
