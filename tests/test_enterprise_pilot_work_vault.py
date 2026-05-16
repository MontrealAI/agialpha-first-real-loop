from agialpha_enterprise_pilot.work_vault import create_work_vault
def test_work_vault_generated():
 w=create_work_vault('p1','j1')
 assert w['settlement_status']=='simulated_local_receipt_only'
