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
