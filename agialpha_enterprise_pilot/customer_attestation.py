from .boundaries import boundary_fields
EXCLUDED=["HR / worker evaluation","profiling of individuals","automated decisions about natural persons","credit / lending","insurance","medical use","legal advice","financial or investment advice","KYC/AML","banking / brokerage / custody","critical infrastructure control","energy or utility market participation","offensive cyber","cybersecurity certification","autonomous procurement","binding contract execution"]
def create_attestation(pilot_id:str)->dict:
 return {"schema_version":"agialpha.customer_use_attestation.v1","pilot_id":pilot_id,"excluded_uses":EXCLUDED,"excluded_uses_acknowledged":True,"status":"accepted",**boundary_fields()}
