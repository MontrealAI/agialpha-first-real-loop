# Developer Guide

## Repo structure
- `agialpha_*` packages: experiment/runtime code.
- `.github/workflows/`: automation and evidence workflows.
- `schemas/`: JSON schemas for manifests, dockets, vault records.
- `docs/`: operator, reviewer, and governance documentation.
- `tests/`: quality, boundary, and regression tests.

## Local setup + checks
```bash
python -m unittest discover -s tests
python -m agialpha_docs audit-workflows --repo-root .
python -m agialpha_docs audit-claims --repo-root .
python -m agialpha_docs audit-links --repo-root .
python -m agialpha_docs audit-readmes --repo-root .
```

## Adding scripts, schemas, workflows
- Add scripts under appropriate package/module and test them.
- Add/update schema under `schemas/` and include tests.
- Add workflow in `.github/workflows/` with least-privilege permissions.
- Update `docs/WORKFLOW_CATALOG.md` for every workflow file.

## Evidence + docs guardrails
- Add Evidence Docket template/paths and artifact manifest fields.
- Keep README/docs links valid and relative.
- Preserve claim boundaries; use conservative wording.
- Avoid stale workflow references by re-running docs audits.
