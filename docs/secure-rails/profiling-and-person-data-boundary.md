# Profiling and Personal Data Boundary

## Policy

SecureRails evaluates software artifacts, agentic work events, Evidence Dockets, ProofBundles, workflow changes, and remediation proposals. SecureRails must not profile natural persons.

## Allowed data

- Repository paths.
- Commit SHAs.
- Pull request URLs.
- Workflow IDs.
- Artifact hashes.
- Redacted finding descriptions.
- Safety counters.
- Evidence completeness statuses.

## Restricted data

- Developer names.
- Email addresses.
- Personal identifiers.
- Productivity metrics.
- Behavior timelines.
- Employment-related scores.

Restricted data may appear incidentally in repository metadata, but should not be used to score, rank, profile, monitor, or decide outcomes for natural persons.

## Data minimization rules

- Prefer artifact IDs and hashes over personal identifiers.
- Redact secrets and sensitive values.
- Use salted hashes for secret-like strings.
- Do not print raw secret-like values.
- Do not build dashboards that rank people.

## GDPR posture

SecureRails should be deployed as an evidence and governance tool, not as solely automated decision-making that produces legal or similarly significant effects for natural persons. Any deployment involving personal data must complete a data-protection review.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
