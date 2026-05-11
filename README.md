# AGI ALPHA First Real Loop

AGI ALPHA First Real Loop is a research-oriented monorepo for deterministic, test-first AGI ALPHA subsystems, including Evidence Mission Control, SecureRails, AGI-GA Foundry, Cyber-GA Sovereign, RSI Governor, Evidence Dockets, ProofBundles, and workflow-based experiments.

## What this repository contains
- Workflow-driven experiment families with replay, falsification, and evidence generation.
- Evidence Mission Control pages, registry assets, and artifact ingestion helpers.
- SecureRails governance and defensive-remediation documentation, templates, and guardrail checks.

## Quickstart (zero to first run)
1. Read [docs/START_HERE.md](docs/START_HERE.md).
2. Open [docs/WORKFLOW_LAUNCHPAD.md](docs/WORKFLOW_LAUNCHPAD.md) and select one workflow.
3. Run it from GitHub Actions (**Run workflow**) or CLI (`gh workflow run <workflow-file>.yml`).
4. Download artifacts and review the Evidence Docket + claim boundary.

## How to run from GitHub UI
1. Go to **Actions**.
2. Choose a workflow listed in [docs/WORKFLOW_CATALOG.md](docs/WORKFLOW_CATALOG.md).
3. Click **Run workflow** (when `workflow_dispatch` exists).
4. Inspect logs, artifacts, safety ledger, and Evidence Docket.

## Experiment families
- AGI-GA Foundry
- Cyber-GA Sovereign
- RSI Governor / RSI Forge
- HELIOS
- Gauntlets (Benchmark/Omega/Phoenix)
- Evidence Mission Control maintenance flows

## SecureRails summary
SecureRails is AGI ALPHA’s AI-agent security governance and proof-bound defensive remediation layer. It makes AI-agent work safe to review, safe to replay, and safe to remediate by converting agent actions, workflow changes, findings, and remediation proposals into ProofBundles, Evidence Dockets, redacted safety ledgers, safe PR proposals, validator reports, and reusable defensive capability.

**Boundary:** SecureRails is not autonomous cybersecurity-certification, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.

## Doctrine and claim boundary
**Doctrine:** “No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.”

See [docs/CLAIM_BOUNDARIES.md](docs/CLAIM_BOUNDARIES.md).

## Quick links
- Start here: [docs/START_HERE.md](docs/START_HERE.md)
- Evidence Mission Control: [docs/EVIDENCE_MISSION_CONTROL.md](docs/EVIDENCE_MISSION_CONTROL.md)
- Workflow launchpad: [docs/WORKFLOW_LAUNCHPAD.md](docs/WORKFLOW_LAUNCHPAD.md)
- Workflow catalog: [docs/WORKFLOW_CATALOG.md](docs/WORKFLOW_CATALOG.md)
- Repository map: [docs/REPOSITORY_MAP.md](docs/REPOSITORY_MAP.md)
- Operator quickstart: [docs/OPERATOR_QUICKSTART.md](docs/OPERATOR_QUICKSTART.md)
- Contributor guide: [docs/CONTRIBUTOR_GUIDE.md](docs/CONTRIBUTOR_GUIDE.md)
- SecureRails docs: [docs/secure-rails/README.md](docs/secure-rails/README.md)
- SecureRails Work Vault Registry: [secure_rails_registry/](secure_rails_registry/)
- Work Vaults / MARK / Sovereigns: [docs/secure-rails/work-vaults-mark-sovereigns.md](docs/secure-rails/work-vaults-mark-sovereigns.md)
- Documentation index: [docs/README.md](docs/README.md)

## How to contribute
See [docs/CONTRIBUTOR_GUIDE.md](docs/CONTRIBUTOR_GUIDE.md), [docs/ADDING_NEW_EXPERIMENTS.md](docs/ADDING_NEW_EXPERIMENTS.md), and open a PR with updated workflow/docs audits.

## How to run tests and audits
```bash
python scripts/secure_rails_claim_boundary_check.py .
python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json
python scripts/secure_rails_no_automerge_check.py .
python scripts/secure_rails_use_case_triage_check.py docs/secure-rails/templates/deployment-intake-example.json
python -m agialpha_docs audit-workflows --repo-root .
python -m agialpha_docs audit-claims --repo-root .
python -m agialpha_docs audit-links --repo-root .
python -m agialpha_docs audit-readmes --repo-root .
python -m unittest discover -s tests
```

## Repository map
See [docs/REPOSITORY_MAP.md](docs/REPOSITORY_MAP.md) for directory-by-directory status labels (implemented, scaffolded, planned, evidence-backed, pending).

## Documentation index
See [docs/README.md](docs/README.md) for the full navigation index by role (operator, reviewer, contributor).

- SecureRails Agentic PR Guard 001: [docs/secure-rails/agentic-pr-guard.md](docs/secure-rails/agentic-pr-guard.md)


- SecureRails supply-chain provenance: [docs/secure-rails/supply-chain-provenance.md](docs/secure-rails/supply-chain-provenance.md)

- Installable SecureRails action: [docs/secure-rails/installable-action.md](docs/secure-rails/installable-action.md)
- Reusable SecureRails workflow: [docs/secure-rails/reusable-workflow.md](docs/secure-rails/reusable-workflow.md)
- Customer pilot installation: [docs/secure-rails/customer-pilot-installation.md](docs/secure-rails/customer-pilot-installation.md)

- SecureRails Customer Pilot Intake 001: see docs/secure-rails/customer-pilot-intake.md.

- SecureRails GitHub App Connector 001: docs/secure-rails/github-app-connector.md

## Using this repository as a template

If this is the canonical repo, enable **Template repository** in GitHub settings.
Create a new repo from the template, then run **SecureRails Template Bootstrap 001** or local CLI:
`python -m secure_rails template-bootstrap init ...`.
See:
- docs/secure-rails/quebecai-template-setup.md
- docs/secure-rails/customer-template-setup.md
- docs/secure-rails/github-pages-setup.md
- docs/secure-rails/actions-and-checks-setup.md

## Template Instance Status
Generated artifacts: `docs/_generated/template-bootstrap/`.

- SecureRails release train docs: [docs/secure-rails/release-train.md](docs/secure-rails/release-train.md)


## SecureRails E2E Pilot Canary 001
See `docs/secure-rails/e2e-pilot-canary.md` and workflow `.github/workflows/securerails-e2e-pilot-canary-001.yml`.


## SecureRails Trust Center
- [SECURITY.md](SECURITY.md)
- [Trust Center](docs/secure-rails/trust-center.md)
- [Vulnerability disclosure policy](docs/secure-rails/vulnerability-disclosure-policy.md)
- [Incident response runbook](docs/secure-rails/incident-response-runbook.md)
- [Customer security FAQ](docs/secure-rails/customer-security-faq.md)
- [Trust Center control matrix](docs/secure-rails/trust-center-control-matrix.md)

- Repository security baseline: [docs/secure-rails/repository-security-baseline.md](docs/secure-rails/repository-security-baseline.md)
