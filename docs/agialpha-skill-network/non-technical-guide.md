# Non-Technical Guide: AGI ALPHA Skill Network

## What this page is for

This guide explains the **AGI ALPHA Engine-003 Skill Network** in plain language.

The short version:
- Each completed job must produce reusable learning.
- Learning is saved as either an accepted skill, a rejected skill candidate, or a failure-learning package.
- Accepted skills can be imported by other agents **inside sandbox constraints**.
- The system only claims local bounded skill compounding when held-out tests show B6 (shared skill) beats B5 (no shared skill) under equal constraints.

## What a “skill” means here

A skill is a **portable proof-bound capability package**, not a model-weight update and not an autonomy certificate.

A skill package is only considered valid when linked to:
- raw evaluator logs,
- a ProofBundle,
- an Evidence Docket,
- replay and falsification outcomes,
- boundary controls (claim, token, regulated).

## Why “every job teaches” matters

Every job must produce one of:
1. Accepted Skill Package
2. Rejected Skill Candidate
3. Failure Learning Package

This ensures failed or partial attempts still teach the network what to reuse, reject, quarantine, or test harder.

## What “instantly shared” means (and does not mean)

“Instantly shared” means:
- a validated skill is published in the Network Skill Vault,
- target agents can import the skill into their manifests,
- imports are tracked as evidence.

It does **not** mean automatic production activation.

Imported skills remain inactive outside sandbox by default and require validators + human review before any broader activation.

## How the main comparison works

The core measured comparison is:
- **B5_no_shared_skill**: target agents run held-out adjacent tasks without imported skill.
- **B6_shared_skill_network**: same tasks and constraints, but with imported skill active in sandbox.

The system computes **NetworkSkillPropagationLift = D(B6) - D(B5)** from raw held-out results.

If replay and falsification pass and required gates hold, local bounded compounding wording may be supported.

## What this system does not claim

This project does **not** claim:
- achieved AGI / ASI / superintelligence,
- empirical SOTA or official benchmark victory,
- certified safety or legal exemption,
- autonomous production deployment,
- token value, investment return, or financial upside.

$AGIALPHA remains utility-only accounting.

## Human review and safety boundaries

Human review is required before persistence/activation outside sandbox.

Boundary controls enforced in reporting:
- claim boundary,
- token boundary,
- regulated-boundary firewall,
- no auto-merge,
- no autonomous persistence.

## How to read the public tab

For non-technical readers, focus on:
1. Claim gate status (supported_local_bounded or not_supported)
2. B6 vs B5 comparison and lift
3. Accepted/rejected/failure-learning counts
4. Replay and falsification status
5. Work Vault utility-only receipt language

Footer doctrine:

**“No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.”**
