# GitHub Pages Settings (Required Baseline)

## Pages source
In **Settings → Pages**:
- Set **Source** to **GitHub Actions**.

## Environment guardrails
In **Settings → Environments → github-pages**:
- Allow deployments from the protected/default branch policy used by `main`.
- Do not require impossible manual approvals for the automation identity if autonomous publishing is expected.
- Keep deployment source constrained to trusted default branch deployments.

## Operational expectation
- PR and non-main branches build/validate only.
- Trusted `main` runs in `evidence-hub-publish.yml` are the only path that deploys to `https://montrealai.github.io/agialpha-first-real-loop/`.
