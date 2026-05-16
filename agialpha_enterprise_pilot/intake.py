from .boundaries import envelope
def make_intake(pilot_id,wf,mode):
 d={'schema_version':'agialpha.enterprise_pilot_intake.v1','pilot_id':pilot_id,'customer_label':'synthetic_customer' if mode=='synthetic_only' else 'redacted_customer','customer_data_mode':mode,'workflow_family':wf,'intended_use':'synthetic enterprise workflow evidence generation','excluded_uses_acknowledged':True,'regulated_boundary_triage_required':True,'proofbundle_required':True,'evidence_docket_required':True,'external_replay_packet_required':True,'customer_review_required':True}; d.update(envelope()); return d
