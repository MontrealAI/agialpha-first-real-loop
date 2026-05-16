def create_validator_plan(pilot_id:str,job_pack_id:str)->dict:
 return {"validator_plan_id":f"validator-{pilot_id}","pilot_id":pilot_id,"job_pack_id":job_pack_id,"checks":["intake","triage","attestation","proofbundle","docket"]}
