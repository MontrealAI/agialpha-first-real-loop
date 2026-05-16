from agialpha_enterprise_pilot.work_vault import create_work_vault

def test_work_vault_utility_only():
    w=create_work_vault("p1","j1")
    assert w["wallet_used"] is False
    assert w["payment_executed"] is False
