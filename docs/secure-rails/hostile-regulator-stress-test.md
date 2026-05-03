# Hostile Regulator Stress Test

## Purpose

This document prepares SecureRails for reclassification arguments. It assumes an aggressive reviewer will focus on function and impact, not labels.

## Attack vector A: “This is employment or worker management.”

Potential argument:

- SecureRails evaluates code contributions.
- SecureRails finds defects in work artifacts.
- SecureRails could influence developer outcomes.

Defense:

- SecureRails evaluates software artifacts and agentic work evidence, not natural persons.
- SecureRails outputs are not suitable for performance evaluation.
- Customer use for HR, worker monitoring, promotion, termination, compensation, or discipline is excluded.
- Customer attestation and contract clauses prohibit HR and worker-management use.
- UI and docs must not rank developers or show personal performance scores.

Required evidence:

- Customer Use Attestation.
- Annex III Triage Record.
- No HR / No Worker Evaluation Policy.
- Audit logs showing human review of remediation and no personal scoring.

## Attack vector B: “This is a critical-infrastructure safety component.”

Potential argument:

- SecureRails affects software supply chains.
- Security tooling could affect infrastructure reliability.

Defense:

- SecureRails is advisory governance and evidence support.
- SecureRails does not operate critical infrastructure.
- SecureRails does not control road traffic, water, gas, heating, electricity, or other safety-critical infrastructure.
- SecureRails outputs require independent validation before production use.
- Any safety-component deployment is excluded by default and requires re-screening.

Required evidence:

- Critical Infrastructure Safety-Component Boundary.
- Customer attestation.
- Deployment intake.
- Independent validation requirement in the contract.

## Attack vector C: “This is profiling or risk scoring of natural persons.”

Potential argument:

- SecureRails labels findings or PRs unsafe.
- SecureRails could attach findings to developers.

Defense:

- Risk scoring applies to artifacts, workflows, ProofBundles, Evidence Dockets, and remediation proposals.
- SecureRails must not score, rank, profile, or monitor natural persons.
- Personal identifiers should be minimized, redacted, or treated as incidental repository metadata.

Required evidence:

- Profiling and Personal Data Boundary.
- Data minimization policy.
- UI screenshots without personal performance scores.

## Attack vector D: “This is a GPAI model provider.”

Potential argument:

- SecureRails uses AI models or orchestrates AI agents.

Defense:

- SecureRails is an orchestration, governance, evidence, and remediation-control layer.
- SecureRails does not place a general-purpose AI model on the market by default.
- Third-party model providers remain responsible for their own model-provider obligations.
- If SecureRails later ships its own general-purpose model, a separate GPAI review is mandatory.

Required evidence:

- GPAI Dependency Boundary.
- Third-party model register.
- Customer deployment architecture.

## Attack vector E: “Marketing says it certifies security.”

Potential argument:

- Public claims imply guaranteed security, certification, or compliance.

Defense:

- SecureRails produces evidence, replay, safe PRs, and human-review workflows.
- SecureRails does not certify security or guarantee outcomes.
- Claim-boundary guard blocks prohibited public claims.

Required evidence:

- Claims and Marketing Guardrails.
- Claim-boundary CI logs.
- Public pages with claim footer.

## Bottom line

SecureRails survives pressure when each deployment consistently shows: intended purpose, excluded uses, human review, no profiling, no critical-infrastructure safety reliance, no certification claim, no auto-merge, and documented re-screening for material changes.

## Claim footer

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
