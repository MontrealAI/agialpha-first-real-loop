# GitHub Pages Deployment Diagnosis

## Failing run
- **Run URL:** https://github.com/MontrealAI/agialpha-first-real-loop/actions/runs/25192121986
- **Workflow:** `evidence-hub-publish`
- **Ref/branch:** `codex/fix-github-pages-evidence-architecture-348bok` (`push` event)
- **Failing job/step:** `build-and-deploy` → `python -m agialpha_evidence_hub backfill --repo-root . --out evidence_registry/registry`

## Root cause
The failing deployment was initiated from a non-main `codex/*` branch push, while the workflow still attempted a combined build-and-deploy pattern. The run failed in backfill before deploy, and the deployment path was not isolated behind a strict trusted-branch deploy gate.

## Exact fix
1. Split central publisher into `build-validate` and `deploy-pages` jobs.
2. Add explicit deploy guard so deployment only runs when all conditions are true:
   - repository is `MontrealAI/agialpha-first-real-loop`
   - ref is `refs/heads/main`
   - event is `push`, `workflow_dispatch`, `schedule`, or `repository_dispatch`
3. Keep PR/non-main behavior build+validate only, with explicit skip message:
   - "Build/validate completed. Deployment skipped because this is not main."
4. Keep only `.github/workflows/evidence-hub-publish.yml` authorized to call:
   - `actions/upload-pages-artifact`
   - `actions/deploy-pages`

## Prevention test added
- `tests/test_evidence_hub_pr_deploy_guard.py` verifies deploy guard conditions and PR skip behavior.
- `scripts/check_pages_architecture.py` + `tests/test_pages_architecture.py` enforce single-workflow Pages deployment architecture.
