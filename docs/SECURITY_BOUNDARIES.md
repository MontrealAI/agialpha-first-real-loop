---
title: "Security Boundaries"
audience: "operator|developer|researcher"
status: "current"
source_of_truth: "docs/SECURITY_BOUNDARIES.md"
last_reviewed: "2026-05-01"
claim_boundary_required: true
---

# Security Boundaries

## Purpose
Security Boundaries for AGI ALPHA documentation system.

## Audience
Operators, developers, researchers, external reviewers, and security reviewers.

## Current status
Current as of 2026-05-01.

## Quick links
- [Root README](../README.md)
- [Workflow Launchpad](../WORKFLOW_LAUNCHPAD.md)
- [Claim boundary](../CLAIM_BOUNDARY.md)

## Hard safety invariants
- raw_secret_leak_count = 0
- external_target_scan_count = 0
- exploit_execution_count = 0
- malware_generation_count = 0
- social_engineering_content_count = 0
- unsafe_automerge_count = 0
- critical_safety_incidents = 0

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
