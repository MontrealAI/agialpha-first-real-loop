# Evidence Mission Control v3 Audit (2026-05-01)

## Scope and method
Repository inspected directly on 2026-05-01 using workflow/config/source tree inspection.

## 1) Workflows in `.github/workflows/`
Total detected: **79** workflow files.

Key groups: autonomous, replay, falsification-audit, scaling, delayed-outcome, safe-pr, lifecycle, external-review, evidence-hub publish.

## 2) Workflows currently deploying GitHub Pages
- `evidence-hub-publish.yml` (contains Pages deploy actions).

## 3) Workflows that emit artifacts
Most experiment workflows include `actions/upload-artifact` (autonomous, replay, falsification, scaling, challenge packs, docs audit, etc.).

## 4) Workflows with `workflow_dispatch`
All detected workflow files currently include `workflow_dispatch`.

## 5) Workflows that appear to be experiment producers
Examples:
- `*-autonomous.yml`
- `seed-runner-autonomous.yml`
- `evidence-factory-autonomous.yml`
- `l4-l7-evidence-autopilot.yml`

## 6) Replay/falsification/scaling/delayed-outcome/external-review/safe-PR/lifecycle workflows
Detected by filename and YAML intent:
- replay: `*replay*.yml`, `independent-replay-autonomous.yml`
- falsification: `*falsification-audit*.yml`, `falsification-audit-autonomous.yml`
- scaling: `*scaling*.yml`
- delayed outcome: `*delayed-outcome*.yml`
- external review: `frontier-external-review.yml`, `l4-external-reviewer-replay.yml`
- safe PR: `*safe-pr*.yml`
- lifecycle: `rsi-governor-001-lifecycle.yml`

## 7) Existing evidence directories
- `sample_outputs/`
- `autonomous/evidence_runs/`
- `rsi-governor-runs/`
- `evidence_registry/`

## 8) Existing docs / Pages output directories
- `docs/`
- `_site/` (generated in current architecture/tests)
- legacy docs subtrees inside autonomous evidence outputs.

## 9) Existing `evidence_registry` state
Present:
- top-level: `registry.json`, `experiments.json`, `runs.json`, `workflows.json`, `latest.json`, `discovered.json`, `CHANGELOG.md`
- nested `evidence_registry/registry/*.json` mirror files.

## 10) Broken routes
No committed automated route-health snapshot found in this audit pass; route health should be produced by hub linkcheck/validation step.

## 11) Shallow placeholder routes
Legacy and discovered pages include shallow placeholders in historical content; must be progressively replaced by canonical summaries when manifest-grade evidence exists.

## 12) High-confidence experiment pages
High-confidence families already represented in repo content/workflows include:
HELIOS, CYBER-SOVEREIGN, BENCHMARK-GAUNTLET, OMEGA-GAUNTLET, PHOENIX-HUB, RSI-GOVERNOR, RSI-FORGE, ASCENSION, EVIDENCE-FACTORY.

## 13) Low-confidence discovered entries
Seed/run subdirectories and historical partial directories exist and must remain segregated as low confidence unless upgraded by explicit manifest/docket evidence.

## 14) Known experiment families
- first-rsi-loop / coldchain-energy-loop
- evidence-factory
- helios
- cyber-sovereign
- benchmark-gauntlet
- omega-gauntlet
- omega-aegis
- phoenix-hub
- rsi-governor
- rsi-forge
- ascension
- frontier/usefulness

## 15) Unknown experiment families
Anything not matching manifest evidence or known family prefixes should be treated as discovered/low-confidence until canonicalized.

## 16) Current failure mode
Primary systemic risk: potential drift between dynamic workflows/artifacts and persistent public pages unless central publisher + needed-update + repair + canary loops are continuously enforced.

## 17) Proposed migration plan
1. Enforce single Pages publisher architecture guard.
2. Keep experiment workflows artifact-emitting only.
3. Ensure evidence manifests are emitted and ingested.
4. Normalize and persist registry for run/workflow/experiment state.
5. Build validated static site from registry only.
6. Add repair workflow for safe non-automerge fixes/issues.
7. Add canary workflow proving autonomous new-manifest discovery and rendering.
