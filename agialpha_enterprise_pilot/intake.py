from .boundaries import boundary_fields

def create_intake(pilot_id:str, workflow_family:str, customer_mode:str)->dict:
 return {"schema_version":"agialpha.enterprise_pilot_intake.v1","pilot_id":pilot_id,"customer_label":"synthetic_customer" if customer_mode=="synthetic_only" else "redacted_customer","customer_data_mode":customer_mode,"workflow_family":workflow_family,"intended_use":"enterprise workflow evidence generation","excluded_uses_acknowledged":True,"regulated_boundary_triage_required":True,"proofbundle_required":True,"evidence_docket_required":True,"external_replay_packet_required":True,"customer_review_required":True,**boundary_fields()}
