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


## SecureRails

SecureRails is AGI ALPHA’s AI-agent security governance and proof-bound defensive remediation layer.

It makes AI-agent work safe to review, safe to replay, and safe to remediate by converting agent actions, workflow changes, findings, and remediation proposals into:

- ProofBundles
- Evidence Dockets
- redacted safety ledgers
- safe PR proposals
- validator reports
- reusable defensive capability
- human-reviewed promotion records

SecureRails is designed as repo-owned defensive evidence infrastructure. It is not autonomous cybersecurity assurance or attestation, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product.

### SecureRails quick links

- [SecureRails user guide](docs/secure-rails/README.md)
- [SecureRails public docs page](docs/secure-rails/index.md)
- [Product boundary](docs/secure-rails/product-boundary.md)
- [EU AI Act positioning](docs/secure-rails/eu-ai-act-positioning.md)
- [Foreseeable misuse and excluded uses](docs/secure-rails/foreseeable-misuse-and-excluded-uses.md)
- [Security and safety boundary](docs/secure-rails/security-safety-boundary.md)
- [Claims and marketing guardrails](docs/secure-rails/claims-and-marketing-guardrails.md)
- [Templates](docs/secure-rails/templates/README.md)

### SecureRails compliance guard

The repository includes a SecureRails compliance guard workflow:

```text
.github/workflows/secure-rails-compliance-guard.yml
```

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


## Experiment families

- **Foundry lifecycle experiments**: orchestration, generation, and promotion in `agialpha_agiga_foundry/`.
- **Safety and sovereign evaluations**: policy, held-out, and falsification validations.
- **Benchmark and gauntlet tracks**: repeatable benchmark execution and scoring.
- **Evidence registry workflows**: inventory and provenance updates in `evidence_registry/`.

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
