# README EVIDENCE HUB

Evidence Hub and Mission Control architecture and publisher boundaries.

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## GitHub Pages publishing model

- Central publisher: `.github/workflows/evidence-hub-publish.yml`
- Build/validate-only mode:
  - `pull_request`
  - non-main refs
  - runs discover/backfill/build/validate/linkcheck
  - does **not** deploy Pages
- Trusted deploy mode:
  - `push` to `main`
  - `workflow_dispatch` on `main`
  - `schedule` on default branch
  - `repository_dispatch` on `main`
  - uploads Pages artifact and deploys via `actions/deploy-pages`

## Why only one workflow may deploy

To prevent race conditions and accidental overwrite of the Mission Control site, only the central publisher may use:
- `actions/upload-pages-artifact`
- `actions/deploy-pages`

Architecture enforcement:
- `python scripts/check_pages_architecture.py`
- `python -m unittest tests/test_pages_architecture.py`
- `python -m unittest tests/test_evidence_hub_pr_deploy_guard.py`

## Operator commands

```bash
python scripts/check_pages_architecture.py
python -m agialpha_evidence_hub build --registry evidence_registry --out _site
python -m agialpha_evidence_hub validate --registry evidence_registry --site _site
python -m agialpha_evidence_hub linkcheck --site _site
```
