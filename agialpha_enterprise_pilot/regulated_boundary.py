def triage(intended_use):
 t=intended_use.lower(); blocked=any(x in t for x in ['legal','medical','hr','credit','insurance','kyc','aml'])
 return {'regulated_boundary_result':'regulated_boundary_blocked' if blocked else 'regulated_boundary_passed','regulated_boundary_blocked':blocked}
