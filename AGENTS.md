# AGENTS

## Repo layout
- `agialpha_*` Python packages implement deterministic workflows and CLIs.
- `docs/` contains operator/reviewer docs and generated-data integration.
- `.github/workflows/` contains lifecycle/replay/falsification workflows.
- `schemas/` contains JSON schemas for artifacts.
- `tests/` contains unittest/pytest-compatible checks.

## Build/test commands
- `python -m unittest discover -s tests`
- `pytest -q` (if pytest is available)
- SecureRails checks in `scripts/secure_rails_*.py`

## SecureRails + boundary rules
- No overclaims (no AGI/ASI/superintelligence/SOTA/certification claims).
- Regulated-boundary firewall: block regulated financial/legal/medical/HR/credit/insurance and similar decisioning.
- Utility-only accounting records; no real payments/custody/wallet/KYC/AML/trading.
- No offensive cyber, no external scanning/exploit/malware/social engineering.
- Human review required; no autonomous persistence; no auto-merge.
- Do not deploy GitHub Pages directly from new workflows.

## Definition of done
- Deterministic runnable artifact generation.
- Boundary fields present in major artifacts.
- Tests and SecureRails checks pass.
- Workflow catalog/docs updated with safe claim boundaries.
