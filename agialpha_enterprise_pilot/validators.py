def build_validator_plan(pilot_id, blocked): return {'validator_plan_id':f'vp-{pilot_id}','status':'documentation_only' if blocked else 'ready'}
