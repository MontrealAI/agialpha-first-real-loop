from .boundaries import envelope
PACKS=['software_quality_pack','evidence_ops_pack','docs_ops_pack','trust_center_readiness_pack','secure_rails_readiness_pack','defensive_security_docs_pack','workflow_catalog_readiness_pack','external_replay_readiness_pack','enterprise_pilot_readiness_pack','commercial_packaging_readiness_pack']
def build_job_pack(pilot_id,wf,mode,boundary_result):
 if wf not in PACKS: raise ValueError('unsupported workflow_family')
 d={'job_pack_id':f'{pilot_id}-{wf}','workflow_family':wf,'synthetic_inputs_used':mode=='synthetic_only','customer_approved_redacted_inputs_used':mode=='customer_approved_redacted','prohibited_actions_checked':True,'regulated_boundary_result':boundary_result,'validator_plan':{'complete':True},'proofbundle_plan':{'complete':True},'evidence_docket_plan':{'complete':True},'customer_review_plan':{'status':'pending'},'external_replay_plan':{'complete':True},'work_vault_plan':{'local_json_only':True},'utility_settlement_receipt_plan':{'complete':True},'commercial_usefulness_hypothesis':'safe pilot evidence assists diligence'}
 d.update(envelope()); return d
