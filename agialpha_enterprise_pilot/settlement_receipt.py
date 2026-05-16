NOTICE='This is a utility-only local accounting receipt for validated work. It is not payment processing, custody, money transmission, securities activity, token-value evidence, investment return, or financial advice.'
def build_receipt(pilot_id,wv): return {'settlement_receipt_id':f'sr-{pilot_id}','pilot_id':pilot_id,'work_vault_id':wv,'receipt_mode':'local_json_only','notice':NOTICE}
