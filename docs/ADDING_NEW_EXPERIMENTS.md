# Adding New Experiments

## 1) Create workflow

- Add a new workflow in `.github/workflows/`.
- Keep least-privilege permissions.
- Do **not** deploy GitHub Pages directly from experiment workflows.
- Ensure `workflow_dispatch` is present for operator use.

## 2) Emit manifest

At workflow end, emit `evidence-run-manifest.json` via:

`python -m agialpha_evidence_hub emit-manifest ...`

Include claim boundary and safety counters where required.

## 3) Upload artifacts

Upload the manifest and experiment outputs as artifacts.

## 4) Register and publish centrally

Use central publisher workflow (`evidence-hub-publish.yml`) to ingest and rebuild site.

## 5) Validate

Run locally:

- `python scripts/check_pages_architecture.py`
- `python -m agialpha_evidence_hub build --registry evidence_registry --out _site`
- `python -m agialpha_evidence_hub validate --registry evidence_registry --site _site`
- `python -m agialpha_evidence_hub linkcheck --site _site`

## Policy invariant

**No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.**
