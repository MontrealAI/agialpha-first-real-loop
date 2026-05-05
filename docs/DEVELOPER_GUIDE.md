# Developer Guide

## What this is for
Developer/Codex operations for experiments, workflows, docs audits, and SecureRails guardrails.

## Repository map
- Packages: `agialpha_*`, `rsi_forge_002`, `agialpha_governance_kernel`
- Workflows: `.github/workflows/`
- Scripts: `scripts/`
- Schemas: `schemas/`
- Docs system: `docs/`, `agialpha_docs/`
- Evidence registry: `evidence_registry/`

## Add new experiment
1. Add package/module.
2. Add schema(s) if needed.
3. Add workflow(s).
4. Emit `evidence-run-manifest.json` output.
5. Update experiment docs and workflow catalog.
6. Run full checks.

## Add new workflow
- Place `.yml` in `.github/workflows/`.
- Document in `docs/WORKFLOW_CATALOG.md` and `docs/WORKFLOW_LAUNCHPAD.md`.
- Ensure only `evidence-hub-publish.yml` is a Pages publisher.

## Required local commands
```bash
python -m unittest discover -s tests
python -m agialpha_docs audit-workflows --repo-root .
python -m agialpha_docs audit-claims --repo-root .
python -m agialpha_docs audit-links --repo-root .
python -m agialpha_docs audit-readmes --repo-root .
python scripts/secure_rails_claim_boundary_check.py .
python scripts/secure_rails_no_automerge_check.py .
python scripts/secure_rails_safety_ledger_check.py docs/secure-rails/templates/safety-ledger-example.json
python scripts/secure_rails_use_case_triage_check.py docs/secure-rails/templates/deployment-intake-example.json
python scripts/secure_rails_work_vault_check.py docs/secure-rails/templates/work-vault-example.json
```

## Debug focus
- Docs-audit failures: missing workflow docs, stale links, oversized/invalid readmes.
- SecureRails guard failures: claim boundary, no-automerge, safety ledger, use-case triage.

## Claim-safe writing rules
- Use bounded language: local/proxy evidence, replayable dockets, human-reviewed promotion.
- Avoid overclaims and unsafe token language.
