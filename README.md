# AGIAlpha First Real Loop

A research-oriented monorepo for deterministic, test-first AGIAlpha subsystems.

If you're non-technical, start with **"5-minute quick check"** below. It is safe and read-only.

## What this repository does (plain English)

This project is a toolkit for running repeatable AI research workflows with strict safety and evidence rules:

- It generates candidate ideas/workflows.
- It evaluates those candidates against held-out tasks.
- It records results in structured "Evidence Dockets."
- It prevents unsupported capability claims.

In short: **we separate what the system can *show* from what anyone is allowed to *claim*.**

## 5-minute quick check (non-technical)

> Goal: confirm your local copy is healthy.

1. Open a terminal in this folder.
2. Run the commands below exactly.
3. If you see `passed` at the end, your copy is working.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip pytest
pytest -q
```

## Quickstart (technical)

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

## Common issues and fixes

- **"command not found: python"**
  - Try `python3` instead of `python`.
- **Permission errors inside virtual environment**
  - Delete `.venv` and recreate it.
- **A test fails unexpectedly**
  - Re-run once with `pytest -q`.
  - If it still fails, include the failing test name and full output in your issue.

## Quick links

- [Contributing guide](CONTRIBUTING.md)
- [Workflow launchpad](WORKFLOW_LAUNCHPAD.md)
- [Evidence docket standard](EVIDENCE_DOCKET_STANDARD.md)
- [AGIGA Foundry README](README_AGIGA_FOUNDRY.md)
- [RSI Governor README](README_RSI_GOVERNOR.md)

## How to run from GitHub UI

If you prefer not to run commands locally:

1. Open the **Actions** tab in GitHub.
2. Select a workflow run relevant to your branch or pull request.
3. Inspect artifacts and logs for validation outputs (tests, docs audits, and evidence checks).
4. Use repository scripts documented in `scripts/README_UPLOAD_WITH_GITHUB_WEB_UI.md` when preparing web-only updates.

## Repository guide

- `agialpha_agiga_foundry/` – core foundry modules and CLI.
- `agialpha_benchmark_gauntlet/` – benchmark harness.
- `agialpha_seed_runner/`, `omega_aegis_001/`, `agialpha_helios/` – executable components.
- `tests/` – regression and policy tests.
- `evidence_registry/` – canonical JSON registries.
- `scripts/` – helper and policy-check scripts.

## Engineering practices

- Keep claims conservative and evidence-linked.
- Add/adjust tests in `tests/` with every behavior change.
- Prefer deterministic outputs and schema-validated artifacts.
- Use relative documentation links and keep README files scoped to their subsystem.

## Documentation index

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
