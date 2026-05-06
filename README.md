# AGI ALPHA First Real Loop

AGIAlpha First Real Loop is a research-oriented monorepo for deterministic, test-first AGI ALPHA subsystems: Evidence Mission Control, SecureRails, AGI-GA Foundry, Cyber-GA Sovereign, RSI Governor, HELIOS, ProofBundles, Evidence Dockets, and workflow-driven evidence production.

## Start here
- New operator: `docs/START_HERE.md`
- Run workflows: `docs/OPERATOR_GUIDE.md`
- Add experiment: `docs/ADDING_NEW_EXPERIMENTS.md`
- Evidence standard: `docs/EVIDENCE_GUIDE.md`
- SecureRails: `docs/secure-rails/README.md`
- Work Vaults / MARK / Sovereigns: `docs/secure-rails/work-vaults-mark-sovereigns.md`
- Workflow catalog: `docs/WORKFLOW_CATALOG.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

## What this repo is
- Evidence-first governance infrastructure for bounded AI-agent experimentation.
- A workflow + artifact system for replay, falsification, and human-reviewed promotion.
- A documentation-backed operating model for Security, governance, and research teams.

## What this repo is not
- Not a claim of unsupported capability milestones.
- Not autonomous cyber-governance certification or offensive cyber capability.
- Not an investment product; `$AGIALPHA` is utility accounting infrastructure only.

## Quick links
- Evidence Mission Control: `docs/EVIDENCE_MISSION_CONTROL.md`
- SecureRails overview: `docs/SECURERAILS_OVERVIEW.md`
- Work Vaults / MARK / Sovereigns: `docs/SECURERAILS_WORK_VAULTS.md`
- Experiment families: `docs/EXPERIMENT_GUIDE.md`
- Documentation index: `docs/README.md` (portal: `docs/index.md`)
- Workflow launchpad: `docs/WORKFLOW_LAUNCHPAD.md`

## How to run from GitHub UI
1. Open **Actions**.
2. Pick a workflow from `docs/WORKFLOW_LAUNCHPAD.md` and `docs/WORKFLOW_CATALOG.md`.
3. Click **Run workflow**.
4. Review logs, artifacts, Evidence Docket, replay status, and safety ledger.

## Run locally
```bash
python -m unittest discover -s tests
python -m agialpha_docs audit-workflows --repo-root .
python -m agialpha_docs audit-claims --repo-root .
python -m agialpha_docs audit-links --repo-root .
python -m agialpha_docs audit-readmes --repo-root .
```

## Claim boundary
No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## Engineering practices
- Test-first workflows and schema validation.
- Documentation and workflow-catalog audits.
- Human-governed claim promotion only.

## License
See `LICENSE`.
