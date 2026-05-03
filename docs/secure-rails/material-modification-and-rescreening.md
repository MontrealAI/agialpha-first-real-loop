# Material Modification and Re-screening

## Principle

SecureRails' regulatory posture is preserved only if material changes are logged and re-screened. Drift is the primary risk.

## Material modification triggers

Re-screen before deployment if SecureRails changes any of the following:

- Intended purpose.
- Target customer sector.
- Human-review requirement.
- Auto-merge or remediation persistence.
- Use of personal data.
- Use in employment, worker management, education, credit, health, law enforcement, migration, essential services, justice, or critical infrastructure.
- Use of external target scanning.
- Use of exploit execution.
- Use of secrets or sensitive data.
- Model provider role.
- Claims about certification, compliance, security, AGI, ASI, empirical SOTA, or safe autonomy.
- `$AGIALPHA` token language.

## Re-screening workflow

1. Record the change.
2. Identify affected product boundary.
3. Run claim-boundary check.
4. Run safety-ledger check.
5. Run no-auto-merge check.
6. Complete Annex III triage.
7. Complete customer/deployment attestation if customer-facing.
8. Escalate to counsel if the change touches excluded uses.
9. Approve or reject the change.
10. Archive the decision record.

## Decision states

```text
no_material_change
material_change_low_risk
material_change_requires_controls
blocked_or_escalate
requires_counsel_review
requires_high_risk_assessment
```

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
