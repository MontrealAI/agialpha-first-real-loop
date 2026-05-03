# AGIGA Foundry

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.

## What this is (plain English)

AGIGA Foundry is a controlled pipeline that:

1. Generates candidate opportunities.
2. Evaluates them with reproducible tasks.
3. Stores artifacts and scores in an Evidence Docket.
4. Requires explicit proof gates before any promotion decision.

This design reduces overclaim risk and keeps results auditable.

## Who should use this

- **Researchers/engineers**: run lifecycle and replay workflows.
- **Reviewers/governance**: inspect docket artifacts and falsification reports.
- **Non-technical stakeholders**: verify that claims are tied to concrete evidence.

## Typical commands

```bash
python -m agialpha_agiga_foundry lifecycle \
  --repo-root . \
  --cycles 1 \
  --candidate-niches 16 \
  --evaluate-niches 6 \
  --local-variants-per-niche 3 \
  --out agiga-foundry-runs/test

python -m agialpha_agiga_foundry replay \
  --docket agiga-foundry-runs/test/agiga-foundry-evidence-docket

python -m agialpha_agiga_foundry falsification-audit \
  --docket agiga-foundry-runs/test/agiga-foundry-evidence-docket
```

## Expected outputs

After `lifecycle`, expect:

- candidate/kernel artifacts,
- evaluation results,
- promotion dossier,
- replay/falsification audit outputs,
- summary score tables.

If these are missing, treat the run as incomplete.

## Safety and claims policy

- Do **not** claim SOTA or capability uplift without a complete Evidence Docket.
- Do **not** skip held-out or falsification stages.
- Preserve run manifests for reproducibility and audit traceability.
