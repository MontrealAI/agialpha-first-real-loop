# Developer Guide

## Scope
Repository structure, packages, workflows, tests, schemas, Evidence Registry, and Evidence Mission Control publishing.

## Required local checks
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

## Implementation notes
- Add workflows under `.github/workflows/` and document each in `docs/WORKFLOW_CATALOG.md`.
- Emit `evidence-run-manifest.json` in experiment outputs.
- Do not let non-central workflows deploy GitHub Pages directly.
- Keep claims bounded and avoid unsafe token language.
