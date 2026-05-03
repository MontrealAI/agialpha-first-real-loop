# SecureRails Customer Deployment Playbook

## Stage 0 — Customer intake

Collect:

- customer legal name;
- jurisdiction;
- industry;
- intended use;
- whether personal data is processed;
- whether customer is essential/important entity under cybersecurity regulation;
- whether deployment touches high-risk AI domains;
- repository scope;
- human reviewer names/roles;
- production-remediation policy;
- data retention requirements.

## Stage 1 — Deployment classification

Use:

- `templates/customer-risk-intake.md`
- `templates/ai-act-triage-checklist.md`
- `templates/dpia-template.md` if personal data is processed.

## Stage 2 — Configuration

Enforce:

- repo-owned scope;
- no external scanning;
- read-only by default;
- safe PR only;
- no auto-merge;
- no secret printing;
- redacted safety ledgers;
- Evidence Docket required for claims;
- human review required for remediation.

## Stage 3 — Pilot

Pilot success requires:

- at least one ProofBundle;
- at least one Evidence Docket;
- safety ledger with all hard counters zero;
- replay instructions;
- human-reviewed safe PR or documented rejection;
- customer sign-off.

## Stage 4 — Production

Production requires:

- signed customer terms;
- prohibited-use agreement;
- incident response channel;
- escalation owner;
- deployment-specific risk classification;
- retention policy;
- monitoring dashboard;
- monthly claim-boundary review.

## Stage 5 — Ongoing governance

Monthly:

- review safety ledgers;
- review PR outcomes;
- review Evidence Dockets;
- review rejected findings;
- review customer use-case drift;
- review public claims;
- review token usage if any.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
