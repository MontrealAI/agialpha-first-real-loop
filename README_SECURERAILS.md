# AGI Alpha SecureRails

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

AGI Alpha SecureRails is the AI-agent security governance platform for proof-bound defensive remediation. It secures autonomous software work by converting agent actions, workflow changes, findings, and remediation proposals into replayable ProofBundles, Evidence Dockets, redacted safety ledgers, safe PRs, and reusable defensive capability — with human-governed promotion and no autonomous claim escalation.

## Why this exists
AI-agent work must be safe to review, safe to replay, and safe to remediate before persistence. SecureRails focuses on bounded, repo-owned, defensive governance rather than offensive activity or autonomous claim promotion.

## Core flow
Finding → Validator → ProofBundle → Evidence Docket → Safety Ledger → Safe PR → Human Review → Capability Archive → vNext Defensive Task.

## Hard boundaries
This system does not claim achieved AGI, achieved ASI, empirical SOTA cybersecurity, offensive cyber capability, real-world security certification, guaranteed security, safe autonomy, or civilization-scale capability.

## Run from GitHub UI
Use workflow dispatch for:
- `cyber-ga-sovereign-001-lifecycle.yml`
- `cyber-ga-sovereign-001-replay.yml`
- `cyber-ga-sovereign-001-falsification-audit.yml`
- `cyber-ga-sovereign-001-safe-pr.yml`
- `cyber-ga-sovereign-001-policy-pr.yml`
- `cyber-ga-sovereign-001-delayed-outcome.yml`
- `cyber-ga-sovereign-001-vnext.yml`

## Run with GitHub CLI
```bash
gh workflow run cyber-ga-sovereign-001-lifecycle.yml \
  -f cycles=3 \
  -f candidate_niches=64 \
  -f evaluate_niches=24 \
  -f local_variants_per_niche=5 \
  -f publish_securerails_tab=true \
  -f publish_cyber_sovereign_tab=true \
  -f open_safe_pr_if_passed=false \
  -f open_policy_pr_if_passed=false
```
