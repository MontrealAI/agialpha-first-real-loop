# START HERE

This guide serves three audiences: non-technical operators, technical contributors, and external reviewers.

## First 10 minutes
1. Open Evidence Mission Control (`docs/EVIDENCE_MISSION_CONTROL.md`).
2. Open GitHub **Actions**.
3. Choose a workflow from `docs/WORKFLOW_LAUNCHPAD.md`.
4. Run `workflow_dispatch` if available.
5. Inspect logs.
6. Download artifacts.
7. Open the Evidence Docket.
8. Review the claim boundary.
9. Check the safety ledger.
10. Record outcome (safe remediation / reject / escalate).

## For non-technical operators
- Read first: `docs/OPERATOR_QUICKSTART.md`.
- Click: Actions → workflow → Run workflow.
- Run: bounded autonomous + replay workflows.
- Expected output: artifacts, manifest, Evidence Docket, safety ledger.
- Do not claim: AGI/ASI/SOTA/certification/investment outcomes.

## For technical contributors
- Read first: `docs/CONTRIBUTOR_GUIDE.md`, `docs/ADDING_NEW_EXPERIMENTS.md`.
- Click: workflow YAMLs in `.github/workflows/` + catalog updates.
- Run: docs audits, SecureRails checks, unit tests.
- Expected output: passing checks, updated docs, replayable artifacts.
- Do not claim: autonomous promotion or legal/certification approval.

## For external reviewers
- Read first: `docs/REVIEWER_REPLAY_GUIDE.md`, `docs/CLAIM_BOUNDARIES.md`.
- Click: run artifacts and replay instructions.
- Run: replay workflows and claim/safety verification.
- Expected output: reproducible replay logs and bounded claims.
- Do not claim: guarantees, exemption status, offensive cyber capabilities.

## Doctrine
**No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.**
