# GitHub Pages Deployment Diagnosis (2026-05-01)

## Failing run inspected
- **Run URL:** https://github.com/MontrealAI/agialpha-first-real-loop/actions/runs/25191403229
- **Workflow:** `evidence-hub-publish`
- **Branch / ref:** `codex/fix-github-pages-evidence-architecture` (`push` event)
- **Failed job:** `deploy`
- **Failed step:** job failed before any steps executed (`steps: []` in Actions Jobs API)

## Failure mode
The workflow attempted to execute the GitHub Pages deploy job on a non-`main` branch (`codex/...`).

The build/publish job completed and uploaded a Pages artifact, but deployment failed at the environment/protection boundary for `github-pages` (untrusted ref deployment attempt), leaving a failed active deployment record.

## Root cause
Deployment gating was insufficiently strict in the failing revision: the deploy path could be reached from an experimental branch run instead of only trusted default-branch contexts.

## Exact fix
`evidence-hub-publish.yml` now enforces a strict deploy guard:
- repository must be `MontrealAI/agialpha-first-real-loop`
- ref must be `refs/heads/main`
- event must be one of: `push`, `workflow_dispatch`, `schedule`, `repository_dispatch`

PR/non-main runs are build+validate only and emit:
> Build/validate completed. Deployment skipped because this is not main.

## Prevention checks
- `scripts/check_pages_architecture.py` fails if any workflow besides `.github/workflows/evidence-hub-publish.yml` contains direct Pages deploy mechanisms.
- `tests/test_pages_architecture.py` enforces exactly one Pages deploy workflow and verifies central publisher ownership.
- `tests/test_evidence_hub_pr_deploy_guard.py` enforces that PR execution paths do not deploy Pages.


## Superseding successful deployment
- **Successful main deployment run URL:** https://github.com/MontrealAI/agialpha-first-real-loop/actions/runs/25202377683
- **Result:** successful `github-pages` deployment from `main` superseded the failed `codex/...` deployment record in the `github-pages` environment.

## Stabilization re-verification snapshot (2026-05-01)
- Confirmed a single Pages deployment workflow policy remains enforced: only `.github/workflows/evidence-hub-publish.yml` includes Pages deploy actions.
- Re-ran the local validation gate (`python scripts/check_pages_architecture.py`) with success.
- Re-ran repository tests (`python -m unittest discover -s tests`) with all tests passing.
- Re-ran Evidence Mission Control build/validate/linkcheck with success.
- Reconfirmed invariant language in public-facing outputs:
  - **No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.**
