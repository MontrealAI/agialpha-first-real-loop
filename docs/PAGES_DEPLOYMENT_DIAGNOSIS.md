# Pages Deployment Diagnosis

## Failing run details

- Failing deployment status log URL: https://github.com/MontrealAI/agialpha-first-real-loop/actions/runs/25191403229/job/73862032851
- Failing workflow: `evidence-hub-publish`
- Failing branch/ref: `codex/fix-github-pages-evidence-architecture`
- Failing job/step: `deploy` job (`actions/deploy-pages`)

## Root cause

The central publisher was allowed to run and deploy from non-`main` branches. GitHub Deployments shows a failed `github-pages` deployment created from a `codex/*` ref (`deployment id 4541692837`), which is not a trusted default-branch deployment path for Pages. This violated the desired architecture (PR/feature branches should build/validate only, not deploy).

## Exact fix

1. Split the workflow into separate build/validate and deploy jobs.
2. Added explicit deploy guard:
   - `github.repository == 'MontrealAI/agialpha-first-real-loop'`
   - `github.ref == 'refs/heads/main'`
   - event is one of `push|workflow_dispatch|schedule|repository_dispatch`
3. Added `pull_request` trigger for build/validate-only mode.
4. Kept official Pages pattern (`actions/upload-pages-artifact` + `actions/deploy-pages`) in **only** `evidence-hub-publish.yml`.
5. Added PR/non-main skip message: “Build/validate completed. Deployment skipped because this is not main.”

## Prevention test added

- `tests/test_evidence_hub_pr_deploy_guard.py`: enforces trusted-main-only deploy condition in central publisher workflow.
- `tests/test_pages_architecture.py` and `scripts/check_pages_architecture.py`: enforce that only the central publisher contains Pages deploy actions.
