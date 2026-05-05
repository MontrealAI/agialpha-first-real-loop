# Developer Guide

## What this is
Developer/Codex reference for adding experiments/workflows, publishing evidence manifests, and passing documentation + SecureRails guardrails.

## Repository structure
- Python packages: `agialpha_*`, `agialpha_docs/`, `agialpha_evidence_hub/`, `agialpha_securerails/`.
- Workflows: `.github/workflows/*.yml`.
- Scripts/checks: `scripts/`.
- Tests: `tests/`.
- Schemas: `schemas/`.
- Evidence registry: `evidence_registry/`.
- Documentation: `docs/` and `docs/_generated/`.

## Add a new experiment
1. Add package/module and runnable CLI path.
2. Emit `evidence-run-manifest.json` as part of run artifacts.
3. Add/update schema contracts.
4. Add workflow in `.github/workflows/`.
5. Document workflow in `docs/WORKFLOW_CATALOG.md` + `docs/WORKFLOW_LAUNCHPAD.md`.
6. Add user-facing docs and role links in `docs/DOCUMENTATION_INDEX.md`.
7. Run all checks below.

## Add a new workflow safely
- Use `workflow_dispatch` for manual run support where applicable.
- Document trigger/inputs/artifacts/claim boundary in catalog.
- Keep GitHub Pages deploy centralized to `evidence-hub-publish.yml` only.
- Do not add auto-merge posture.

## Evidence Mission Control + Evidence Registry
- Evidence Mission Control docs: `docs/EVIDENCE_MISSION_CONTROL.md`.
- Registry/data artifacts live under `evidence_registry/` and workflow outputs.
- Prefer human-readable pages first; do not make raw JSON the primary UI.

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

## Debugging docs-audit and SecureRails guard
- Docs audit issues: missing workflow docs, broken links, README boundary omissions.
- SecureRails failures: run each check script directly and fix the exact file named by the script.
- See `docs/DEBUGGING_GUIDE.md` for common failure remediations.

## Claim and token language safety
- Allowed: bounded local/proxy CI evidence, replayable dockets, proof-bound defensive remediation.
- Forbidden: achieved AGI/ASI, empirical SOTA without full evidence chain, cybersecurity certification, guaranteed security, token investment framing.
- See `docs/CLAIM_BOUNDARY_STYLE_GUIDE.md` and `docs/secure-rails/token-utility-policy.md`.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
