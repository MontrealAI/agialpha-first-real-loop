# Developer Guide

This guide is for contributors maintaining workflows, evidence outputs, schemas, and governance boundaries.

## Repository structure
- `.github/workflows/`: workflow entrypoints for autonomous runs, replay, falsification, publishing, and compliance checks.
- `docs/`: operator and reviewer documentation, workflow catalog, claim boundaries, and architecture references.
- `docs/secure-rails/`: SecureRails governance, boundary policies, templates, and runbooks.
- `schemas/`: JSON schemas for Evidence Dockets, Work Vault objects, MARK allocation, sovereign assignment, and settlement objects.
- `scripts/`: automation helpers, including SecureRails and evidence maintenance scripts.
- `tests/`: docs audits, workflow coverage checks, schema checks, and overclaim guardrails.

## Local setup
1. Use Python 3.11+.
2. Install project requirements if needed.
3. Run unit tests and docs audits before opening a PR.

## Required local checks
```bash
python -m unittest discover -s tests
python -m agialpha_docs audit-workflows --repo-root .
python -m agialpha_docs audit-claims --repo-root .
python -m agialpha_docs audit-links --repo-root .
python -m agialpha_docs audit-readmes --repo-root .
```

If an `agialpha_docs` command differs in your branch, run `python -m agialpha_docs --help` and use the equivalent command.

## How to add a script safely
1. Place script in an existing module/package with related functionality.
2. Add/update tests in `tests/` for both happy path and boundary behavior.
3. Document script purpose and operational boundary in docs where users will discover it.
4. Never add logic that bypasses safety ledgers, replay checks, or claim boundaries.

## How to add or change schemas
1. Add/update schema under `schemas/`.
2. Add fixtures/examples and validation tests.
3. Ensure existing artifacts remain parseable or provide migration notes.
4. Reference schema pointers in user docs (especially Evidence and SecureRails docs).

## How to add workflows
1. Add a new file in `.github/workflows/` with least-privilege permissions.
2. Use `workflow_dispatch` inputs with conservative defaults.
3. Upload required artifacts, including evidence manifest/docket where applicable.
4. Update `docs/WORKFLOW_CATALOG.md` in the same PR.
5. Ensure no direct Pages deployment is added outside central publisher workflows.

## Keeping docs-audit green
- Every workflow must be catalogued and linked.
- Keep README/doc links relative and valid.
- Use exact project terminology (SecureRails, Evidence Docket, ProofBundle, Work Vault, ALPHA AGI MARK, ALPHA AGI Sovereign).
- Prefer scannable tables/checklists over long prose.

## Claim boundary preservation
- No Evidence Docket, no empirical SOTA claim.
- Autonomous evidence production is allowed; autonomous claim promotion is not.
- Never claim achieved AGI/ASI, guaranteed security, certification, offensive cyber capability, or EU AI Act exemption.
- Keep `$AGIALPHA` language strictly utility/accounting oriented.

## Avoiding stale docs and broken links
- When adding/moving files, update `README.md`, `docs/README.md`, and any affected runbooks.
- Re-run docs link audits locally.
- Remove duplicates only when replaced with a canonical page and record that in `docs/CONTENT_PRESERVATION_LEDGER.md`.
