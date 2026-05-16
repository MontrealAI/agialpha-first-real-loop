from .boundaries import boundary_fields
TEXT="This pilot evidence may support commercial-readiness and implementation-side valuation-support analysis. It does not assert valuation, investment return, token value, revenue, ARR, ROI, fair market value, or financial advice."
def create_link(pilot_id:str,tier:str)->dict:
 return {"pilot_id":pilot_id,"commercial_readiness_tier":tier,"customer_review_status":"pending","external_replay_status":"generated","repeatable_deployment_status":"repeatable","paid_pilot_or_commercial_commitment_status":"not_reported","missing_evidence":["paid_pilot_or_commercial_commitment_status:not_reported"],"statement":TEXT,"not_an_investment_claim":True,**boundary_fields()}
