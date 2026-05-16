from .boundaries import boundary_fields
def create_work_vault(pilot_id:str,job_pack_id:str)->dict:
 return {"work_vault_id":f"workvault-{pilot_id}","pilot_id":pilot_id,"job_pack_id":job_pack_id,"alpha_work_units_estimate":100,"validator_fee_units":5,"replay_fee_units":5,"proofbundle_fee_units":8,"evidence_docket_fee_units":8,"archive_access_units":2,"unused_budget_refund_units":0,"settlement_status":"simulated_local_receipt_only",**boundary_fields()}
