# Evidence Hub

## Evidence Hub publishing architecture

Root cause: multiple workflows were independently deploying GitHub Pages and overwriting root content.

Fix: all experiment workflows now emit evidence manifests/artifacts, and only `.github/workflows/evidence-hub-publish.yml` deploys Pages from persistent `evidence_registry/registry`.

To add a new workflow:
1. Generate `evidence_run_manifest.json`.
2. Upload it as an artifact.
3. Do **not** call `actions/deploy-pages`.
4. Let `evidence-hub-publish` aggregate + deploy.

Claim boundary: No Evidence Docket, no empirical SOTA claim.
