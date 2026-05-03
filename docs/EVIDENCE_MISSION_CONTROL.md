---
title: "Evidence Mission Control"
audience: "operator|developer|researcher"
status: "current"
source_of_truth: "docs/EVIDENCE_MISSION_CONTROL.md"
last_reviewed: "2026-05-01"
claim_boundary_required: true
---

# Evidence Mission Control

## Purpose
Evidence Mission Control for AGI ALPHA documentation system.

## Audience
Operators, developers, researchers, external reviewers, and security reviewers.

## Current status
Current as of 2026-05-01.

## Quick links
- [Root README](../README.md)
- [Workflow Launchpad](../WORKFLOW_LAUNCHPAD.md)
- [Claim boundary](../CLAIM_BOUNDARY.md)

## SecureRails Work Vault ingest

When a SecureRails Work Vault run is produced, ingest the deterministic output record into Mission Control with these pointers:

- Work Vault run: `work_vault.run_id`
- Vault scope: `work_vault.defensive_scope`
- MARK allocation: `mark_allocation.mark_id`
- Sovereign assignment: `sovereign_assignment.sovereign_id`
- AGI job + state: `agi_job.job_id`, `agi_job.status`
- Proof reference: `proof_bundle.proof_bundle_id`, `proof_bundle.sha256`
- Evidence docket reference: `evidence_docket.docket_id`
- Human review gate: `human_review.decision`, `human_review.reviewed_by`
- Utility receipt: `utility_settlement.receipt_id`

Operator rule: if `evidence_docket` is absent or malformed, reject ingest and do not promote remediation.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.


No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
