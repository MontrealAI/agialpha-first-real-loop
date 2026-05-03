# AGIAlpha First Real Loop

A research-oriented monorepo for deterministic, test-first AGIAlpha subsystems, including:

- **AGIGA Foundry** lifecycle orchestration and evidence generation.
- **Cyber GA Sovereign** safety/evaluation artifacts.
- **RSI Governor** checks for overclaim boundaries, lifecycle controls, and run integrity.
- **Evidence Hub/Registry** static artifacts and machine-readable run outputs.

## Quickstart

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip pytest
```

### 2) Run the full test suite

```bash
pytest -q
```

### 3) Run selected entry points

```bash
python -m agialpha_benchmark_gauntlet --help
python -m agialpha_seed_runner --help
python -m omega_aegis_001 --help
```


## Quick links

- [Contributing guide](CONTRIBUTING.md)
- [Workflow launchpad](WORKFLOW_LAUNCHPAD.md)
- [Evidence docket standard](EVIDENCE_DOCKET_STANDARD.md)
- [AGIGA Foundry README](README_AGIGA_FOUNDRY.md)

## How to run from GitHub UI

If you prefer not to run commands locally:

1. Open the **Actions** tab in GitHub.
2. Select a workflow run relevant to your branch or pull request.
3. Inspect artifacts and logs for validation outputs (tests, docs audits, and evidence checks).
4. Use repository scripts documented in `scripts/README_UPLOAD_WITH_GITHUB_WEB_UI.md` when preparing web-only updates.

## Experiment families

- **Foundry lifecycle experiments**: orchestration, generation, and promotion in `agialpha_agiga_foundry/`.
- **Safety and sovereign evaluations**: policy, held-out, and falsification validations.
- **Benchmark and gauntlet tracks**: repeatable benchmark execution and scoring.
- **Evidence registry workflows**: inventory and provenance updates in `evidence_registry/`.

## Repository Guide

- `agialpha_agiga_foundry/` – core foundry modules and CLI.
- `agialpha_benchmark_gauntlet/` – benchmark harness.
- `agialpha_seed_runner/`, `omega_aegis_001/`, `agialpha_helios/` – executable components.
- `tests/` – regression and policy tests.
- `evidence_registry/` – canonical JSON registries.
- `scripts/` – helper and policy-check scripts.

## Engineering Practices

- Keep claims conservative and evidence-linked.
- Add/adjust tests in `tests/` with every behavior change.
- Prefer deterministic outputs and schema-validated artifacts.
- Use relative documentation links and keep README files scoped to their subsystem.

## Documentation Index

- `CONTRIBUTING.md`
- `EVIDENCE_DOCKET_STANDARD.md`
- `WORKFLOW_LAUNCHPAD.md`
- `README_AGIGA_FOUNDRY.md`
- `README_BENCHMARK_GAUNTLET_001.md`
- `README_RSI_GOVERNOR.md`
- `README_OMEGA_GAUNTLET_001.md`
- `README_L4_L7_AUTOPILOT.md`
- `README_ASCENSION_001.md`

## License

Distributed under the terms in `LICENSE`.
