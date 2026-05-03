# EU AI Act Annex III Triage

## Objective

This triage determines whether a deployment remains inside SecureRails' default intended purpose or must be blocked/escalated for high-risk review.

## Default answer

For standard repo-owned defensive governance deployments, SecureRails is not intended to be an Annex III high-risk AI system. It is an advisory and evidence-support system for software-work review and human-governed remediation.

## Triage table

| Annex III area | SecureRails default posture | Block / escalate if |
|---|---|---|
| Biometrics | Not applicable. | Any biometric identification, categorization, emotion recognition, or biometric inference is requested. |
| Critical infrastructure | Not a safety component by intended purpose. | Customer wants to use outputs as safety-control, operational-control, or safety-component decisions. |
| Education and vocational training | Not applicable. | Customer wants to evaluate learners or decide access. |
| Employment and worker management | Excluded. | Customer wants to evaluate, rank, monitor, allocate tasks to, discipline, promote, terminate, or compensate natural persons. |
| Essential services | Not applicable. | Customer wants to decide access to benefits, credit, insurance, or essential services. |
| Law enforcement | Not applicable. | Customer wants investigative, risk-assessment, prediction, evidence-reliability, or enforcement use. |
| Migration, asylum, border control | Not applicable. | Customer wants border, asylum, immigration, or identity-document decision support. |
| Justice and democratic processes | Not applicable. | Customer wants legal decision support, judicial fact/law application, or election/campaign manipulation use. |

## Required record

Each deployment must retain:

- deployment-intake form;
- Annex III triage form;
- customer use attestation;
- foreseeable misuse register;
- material modification log;
- human-review configuration evidence;
- no-auto-merge evidence.

## Decision states

```text
allowed_default
allowed_with_controls
blocked_or_escalate
requires_counsel_review
requires_high_risk_assessment
```

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
