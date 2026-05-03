# SecureRails Operator Runbook

## Daily checks

- [ ] Evidence Mission Control public site is live.
- [ ] SecureRails route is live.
- [ ] Compliance Guard workflow is green.
- [ ] No direct Pages deploy conflict.
- [ ] No unsafe public claim.
- [ ] No nonzero hard safety invariant.
- [ ] No unreviewed safe PR merged.

## Running the compliance guard

```bash
python scripts/secure_rails_claim_boundary_check.py .
python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json
```

## Running through GitHub Actions

Open Actions and run:

```text
SecureRails Compliance Guard
```

## When a finding appears

1. Confirm it is repo-owned and defensive.
2. Confirm no raw secret is printed.
3. Create or update Evidence Docket.
4. Create safe PR proposal only if safe.
5. Human reviewer approves, rejects, or requests changes.
6. Record decision.
7. Archive accepted and rejected artifacts.

## Emergency stop

Stop promotion if any appears:

- raw secret leak;
- external target scan;
- exploit execution;
- malware generation;
- social engineering;
- unsafe auto-merge;
- public overclaim;
- token investment language.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
