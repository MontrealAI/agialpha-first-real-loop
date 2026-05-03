# Data Protection and Privacy Posture

## Default privacy posture

SecureRails should avoid processing personal data unless necessary for customer deployment. It should not profile natural persons, rank workers, make employment decisions, or make solely automated decisions with legal or similarly significant effects.

## Data minimization

Collect only:

- repo metadata required for defensive review;
- workflow metadata;
- artifact metadata;
- redacted security findings;
- ProofBundle and Evidence Docket metadata;
- human review status.

Avoid:

- personal profiling;
- unnecessary log ingestion;
- private communications;
- personal performance scoring;
- raw secrets;
- raw credentials.

## DPIA triggers

Complete a DPIA if:

- customer requires processing personal data;
- deployment involves employee monitoring;
- deployment involves critical infrastructure;
- deployment uses sensitive data;
- deployment could materially affect individuals.

## Retention

Default retention:

- public Evidence Dockets: permanent unless redaction or legal issue arises;
- customer private dockets: contract-defined;
- raw logs: shortest feasible period;
- raw secrets: never stored.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
