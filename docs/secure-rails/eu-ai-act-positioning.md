# EU AI Act Positioning for SecureRails

## Executive position

SecureRails is designed to remain outside EU AI Act high-risk and GPAI-provider categories by default. It is a defensive governance and evidence system for agentic software work. It does not make autonomous decisions about people, does not perform prohibited practices, does not provide GPAI models by default, and does not certify cybersecurity.

The central legal-control principle is consistency: the real deployment must match the intended purpose. If a customer wants SecureRails to influence employment, worker management, profiling, critical-infrastructure safety, essential services, law enforcement, education, migration, credit, medical decisions, or another regulated category, the deployment must be blocked or re-screened before production.

## Default classification

| Question | SecureRails default answer | Result |
|---|---|---|
| Is it a GPAI model provider? | No, SecureRails orchestrates and governs agentic work; it does not place a general-purpose model on the market by default. | GPAI-provider obligations are not default. |
| Is it high-risk under Annex III by intended purpose? | No, not when used for software-work evidence, replay, redaction, and human-reviewed remediation. | High-risk obligations are not default. |
| Does it make legal or similarly significant decisions? | No. Human review is required. | Avoid automated decision-making exposure. |
| Does it profile natural persons? | No. Developer identities must not be scored or ranked. | Profiling boundary preserved. |
| Is it a safety component of critical infrastructure? | No. Outputs are advisory and require independent validation. | Critical-infrastructure safety-component boundary preserved. |
| Does it perform prohibited practices? | No. | Must remain prohibited-use-free. |

## High-risk triggers to avoid

Do not deploy SecureRails as a system that decides, materially influences, or substitutes for human judgment in:

- employment or worker management;
- performance evaluation of developers, contractors, validators, or operators;
- creditworthiness or financial eligibility;
- education access or assessment;
- access to essential public or private services;
- law enforcement, migration, asylum, border control, or justice decisions;
- biometric identification, categorization, or emotion recognition;
- medical, safety-critical, or critical-infrastructure control decisions;
- critical infrastructure safety operation, including road traffic, water, gas, heating, electricity, or similar safety components.

## Article 6(3)-style posture

Where SecureRails appears near a listed domain, the deployment should be framed and documented as narrow, procedural, preparatory, or improvement-support only. It must not materially influence high-impact decisions about natural persons or safety-critical outcomes. It must preserve human review.

## If a customer insists on high-risk or safety-critical deployment

Escalate before production:

1. identify the intended purpose;
2. complete Annex III triage;
3. document foreseeable misuse;
4. identify provider/deployer roles;
5. prepare risk-management file;
6. document human oversight;
7. validate data governance;
8. conduct conformity assessment if required;
9. update customer contract;
10. do not ship until counsel approves.

## Required public boundary

> SecureRails is a defensive AI-agent security governance system for software-work evidence, replay, and human-reviewed remediation. It does not make autonomous legal, employment, credit, biometric, medical, law-enforcement, education, migration, essential-service, or critical-infrastructure safety decisions; it does not provide cybersecurity certification; it does not perform offensive cyber activity; and it does not promote autonomous production changes without human review.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
