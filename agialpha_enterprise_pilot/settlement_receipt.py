from .boundaries import boundary_fields
TEXT="This is a utility-only local accounting receipt for validated work. No wallet, custody, payment processing, money transmission, securities activity, token-value evidence, investment return, ROI, yield, or financial advice."
def create_receipt(pilot_id:str,work_vault_id:str)->dict:
 return {"settlement_receipt_id":f"receipt-{pilot_id}","pilot_id":pilot_id,"work_vault_id":work_vault_id,"receipt_text":TEXT,"notice":TEXT,"status":"simulated_local_receipt_only",**boundary_fields()}
