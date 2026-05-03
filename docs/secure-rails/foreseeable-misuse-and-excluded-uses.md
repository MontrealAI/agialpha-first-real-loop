# Foreseeable Misuse & Excluded Uses

## Purpose

This page closes the main hostile-regulator gap: the claim that misuse was reasonably foreseeable. SecureRails must document foreseeable misuse, prohibit it, and require customer attestation before deployment.

## Foreseeable misuse register

| Misuse | Why it matters | Required control | Deployment status |
|---|---|---|---|
| Employee or contractor performance evaluation | Could be characterized as employment or worker-management use. | Prohibited. Outputs are not suitable for evaluating workers or assigning personnel consequences. | Block or re-screen. |
| Ranking developers by code quality, findings, speed, or security risk | Could be characterized as profiling or worker monitoring. | Prohibited. Do not link findings to personal performance scores. | Block or re-screen. |
| Automated enforcement decisions | Could become automated decision-making. | Prohibited. Human review required. | Block or re-screen. |
| Critical-infrastructure safety reliance | Could be characterized as a safety component. | Prohibited by default. Outputs advisory only and require independent validation. | Block or re-screen. |
| Real-world security certification | Creates certification and liability exposure. | Prohibited. SecureRails produces evidence, not certification. | Block. |
| Offensive cyber use | Creates safety, legal, and policy exposure. | Prohibited. Repo-owned defensive scope only. | Block. |
| External target scanning | Could be unauthorized security activity. | Prohibited unless separately authorized and reclassified. | Block. |
| Exploit execution | Offensive or unsafe behavior. | Prohibited. | Block. |
| Secret harvesting or disclosure | Data-protection and security risk. | Prohibited. Redaction and salted hash only. | Block. |
| Auto-merge of remediation | Weakens human-governed posture. | Prohibited. Human review required. | Block. |
| Token investment claims | Securities and consumer-protection exposure. | Prohibited. Utility-only language. | Block. |

## Excluded uses

SecureRails must not be used for:

- HR, hiring, promotion, termination, compensation, worker monitoring, or performance evaluation.
- Profiling natural persons.
- Decisions affecting access to credit, insurance, public benefits, education, employment, essential services, justice, migration, or law enforcement.
- Critical-infrastructure safety control or safety-component operation.
- Medical, legal, or similarly significant decision-making.
- Offensive security, external scanning, exploit execution, credential collection, malware generation, or social engineering.
- Automated production remediation without human review.
- Cybersecurity certification or guarantee of security.

## Customer-facing excluded-use clause

> Customer will not use SecureRails or its outputs to evaluate, rank, monitor, profile, discipline, promote, terminate, compensate, or otherwise make decisions about natural persons, including employees, contractors, developers, validators, or operators. Customer will not use SecureRails as a safety component of critical infrastructure or as a substitute for independent security validation. Customer will not use SecureRails for offensive cyber activity, external target scanning, exploit execution, credential collection, malware generation, social engineering, or automated remediation without human review.

## Operator rule

If a proposed deployment touches any excluded use, classify it as `blocked_or_escalate` until counsel approves a separate posture.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
