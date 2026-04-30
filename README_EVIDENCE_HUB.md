# Evidence Hub publishing architecture

Central publisher workflow: `.github/workflows/evidence-hub-publish.yml`.

- Experiment workflows emit evidence manifests and artifacts.
- Persistent registry lives in `evidence_registry/registry`.
- Static site is built from registry using `python -m agialpha_evidence_hub build`.
- Only central publisher deploys GitHub Pages.

## Add a future workflow
1. Generate a manifest matching `schemas/evidence_run_manifest.schema.json`.
2. Upload manifest as artifact.
3. Invoke `python -m agialpha_evidence_hub register-run --input <manifest>`.
4. Let central publisher rebuild Pages.

No Evidence Docket, no empirical SOTA claim.
