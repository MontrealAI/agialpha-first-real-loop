# Developer Guide

## Repository structure (high level)
- `.github/workflows/`: automation, evidence pipelines, publishing.
- `docs/`: operator + developer + governance documentation.
- `scripts/`: evidence, SecureRails, rendering, and guardrail helpers.
- `tests/`: unit/integration/doc-audit enforcement.

## Local setup
This repository currently does **not** ship a `requirements.txt` or lockfile. Start with a clean virtualenv, then run tests/audits and install any missing packages reported by Python.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m unittest discover -s tests
```

If a command reports a missing module, install that package explicitly in your active environment and record the dependency source in your PR notes.

## Core test and docs checks
Run these before pushing:
```bash
python -m unittest discover -s tests
python -m agialpha_docs audit-workflows --repo-root .
python -m agialpha_docs audit-claims --repo-root .
python -m agialpha_docs audit-links --repo-root .
python -m agialpha_docs audit-readmes --repo-root .
```

## Docs-audit expectations
- Every workflow in `.github/workflows/` must appear in `docs/WORKFLOW_CATALOG.md`.
- Root README and docs links must resolve.
- Required docs must exist and remain navigable for non-technical operators.
- Claim-boundary language must block overclaims and allow explicit negative-boundary statements.

## Adding scripts safely
1. Place script in `scripts/` with clear name and docstring.
2. Add/extend tests in `tests/`.
3. Document usage in relevant guide and workflow docs.
4. Ensure logs/artifacts are bounded and auditable.

## Adding schemas / docket templates
1. Add schema/template in the established schema/template path.
2. Add validation tests.
3. Reference schema in Evidence/secure-rails docs.
4. Update replay/falsification expectations if schema semantics changed.

## Adding workflows
Follow `docs/ADDING_NEW_WORKFLOWS.md`.

Minimum requirements:
- Documented `workflow_dispatch` inputs.
- Least-privilege permissions.
- Artifact uploads for evidence-bearing runs.
- Claim-boundary-safe language in outputs/logs.
- Workflow catalog entry + related docs links.

## Keeping claim boundaries intact
- Never imply AGI/ASI achievement.
- Never imply unsupported top-tier benchmark claim without docket-backed external evidence and approved phrasing.
- Keep `$AGIALPHA` language in utility/accounting terms only.
- Keep SecureRails framed as governance + proof-bound defensive remediation.

## Avoid stale workflows and broken links
- Remove or update docs references when workflow files are renamed.
- Update workflow catalog in same PR as workflow changes.
- Run link audits locally.

## Content preservation note policy
If you relocate or replace substantive docs, add a short note in changelog/PR body indicating where content moved.
