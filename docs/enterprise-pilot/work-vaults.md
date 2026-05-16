# Work Vaults

Work Vault records are deterministic accounting artifacts for pilot utility work units.

They must remain utility-only and synthetic in this implementation:
- no wallet/custody/payment execution
- no token price/value logic
- no investment claims

Reference implementation details are in:
- `docs/enterprise-pilot/work-vaults-and-utility-receipts.md`
- `agialpha_enterprise_pilot/work_vault.py`
- `agialpha_enterprise_pilot/settlement.py`
