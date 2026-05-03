# No HR / No Worker Evaluation Policy

## Policy

SecureRails outputs are not designed, validated, or permitted for HR, employment, worker-management, productivity-scoring, performance-evaluation, compensation, promotion, termination, discipline, or task-allocation decisions about natural persons.

## Why this matters

A regulator, customer, or employee could argue that repository findings indirectly evaluate developers. This policy prevents that drift.

## Allowed

- Assessing a repo-owned workflow artifact.
- Assessing a proposed remediation patch.
- Assessing an Evidence Docket.
- Assessing a ProofBundle.
- Assessing whether a safe PR needs human review.

## Not allowed

- Ranking developers.
- Scoring employee quality.
- Monitoring worker performance.
- Linking findings to disciplinary action.
- Assigning tasks based on personal traits or behavior.
- Deciding promotion, termination, compensation, or review outcomes.

## UI rule

Dashboards should show artifact risk, workflow risk, evidence completeness, and remediation status. They should not show personal performance scores for named individuals.

## Customer clause

> SecureRails outputs are not suitable for performance evaluation or worker-management use. Customer will not use SecureRails to evaluate, rank, monitor, discipline, promote, terminate, compensate, or make decisions about natural persons.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
