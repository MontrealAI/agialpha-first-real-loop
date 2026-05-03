# AI Act Triage Checklist

## Deployment identity

- customer:
- jurisdiction:
- intended purpose:
- user group:
- affected persons:
- model provider:
- deployer:
- operator:

## Prohibited-use check

- [ ] No subliminal/manipulative harmful use.
- [ ] No social scoring.
- [ ] No prohibited biometric categorization.
- [ ] No unlawful law-enforcement biometric identification.
- [ ] No emotion recognition in prohibited contexts.

## High-risk check

Does the system make or materially influence decisions in any of these domains?

- [ ] biometric identification/categorization;
- [ ] critical infrastructure safety;
- [ ] education/vocational training;
- [ ] employment/worker management;
- [ ] essential public/private services;
- [ ] law enforcement;
- [ ] migration/asylum/border;
- [ ] administration of justice/democratic processes;
- [ ] regulated product safety component.

If any box is checked, escalate before deployment.

## GPAI check

- [ ] SecureRails is not providing a general-purpose model.
- [ ] No model weights are placed on market by SecureRails.
- [ ] If a model is provided, GPAI obligations are separately assessed.

## Transparency check

- [ ] Users know when they interact with AI-generated reports or PR drafts.
- [ ] Generated content is labeled where appropriate.

## Human oversight

- [ ] Safe PRs require human review.
- [ ] Claims require human review.
- [ ] Production remediation requires human review.

## Final classification

- [ ] Low / limited risk governance support.
- [ ] High-risk use case escalated.
- [ ] GPAI-provider assessment required.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
