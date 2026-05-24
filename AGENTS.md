# AGENTS

## Repo purpose
- Provide deterministic AGI ALPHA evidence engines, safety rails, replay/falsification workflows, and public evidence artifacts with strict claim and boundary controls.

## Repo layout
- `agialpha_*` Python packages implement deterministic workflows and CLIs.
- `docs/` contains operator/reviewer docs and generated-data integration.
- `.github/workflows/` contains lifecycle/replay/falsification workflows.
- `schemas/` contains JSON schemas for artifacts.
- `tests/` contains unittest/pytest-compatible checks.

## Build/test commands
- `python -m unittest discover -s tests`
- `pytest -q` (if pytest is available)
- `python -m agialpha_engine network-compounding-run --repo-root . --registry agialpha_skill_network_registry --out /tmp/agialpha-skill-network-test --jobs 5 --target-agents 3 --heldout-tasks 5 --seed 123`
- `python -m agialpha_engine network-compounding-replay --run /tmp/agialpha-skill-network-test`
- `python -m agialpha_engine network-compounding-falsification-audit --run /tmp/agialpha-skill-network-test`
- `python -m agialpha_engine network-compounding-validate --run /tmp/agialpha-skill-network-test`
- `python -m agialpha_engine network-compounding-build-data --registry agialpha_skill_network_registry --out docs/_generated/agialpha-skill-network`
- SecureRails checks in `scripts/secure_rails_*.py`

## SecureRails + boundary rules
- No overclaims (no AGI/ASI/superintelligence/SOTA/certification claims).
- Regulated-boundary firewall: block regulated financial/legal/medical/HR/credit/insurance and similar decisioning.
- Utility-only accounting records; no wallet/custody/payment/trading/KYC/AML logic or execution paths.
- No offensive cyber, no external scanning/exploit/malware/social engineering.
- Human review required; no autonomous persistence; no auto-merge.
- Do not deploy GitHub Pages directly from new workflows.

## Definition of done
- Deterministic runnable artifact generation.
- Boundary fields present in major artifacts.
- Tests and SecureRails checks pass.
- Workflow catalog/docs updated with safe claim boundaries.
