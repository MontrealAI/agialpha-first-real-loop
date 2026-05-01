# GitHub Pages Settings Baseline

Use these settings to keep Evidence Mission Control deployments trusted and stable.

## Settings → Pages
- **Source:** `GitHub Actions`

## Settings → Environments → `github-pages`
- Allow deployments from the **default/protected branch** path used by the publisher (`main`).
- Do **not** require impossible manual approvals for bot-driven autonomous publish runs if unattended deployment is expected.
- Keep deployment scope constrained to trusted branch execution (central publisher guard already enforces this in CI).

## Repository workflow architecture expectation
- Only `.github/workflows/evidence-hub-publish.yml` may upload/deploy Pages artifacts.
- PR branches may build/validate, but may not deploy.
- Main/trusted events deploy through `actions/upload-pages-artifact` + `actions/deploy-pages` with `github-pages` environment.
