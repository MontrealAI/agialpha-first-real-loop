from .boundaries import boundary_fields
def create_proofbundle(pilot_id:str,job_pack_id:str)->dict:
 return {"proofbundle_id":f"proofbundle-{pilot_id}","pilot_id":pilot_id,"job_pack_id":job_pack_id,"proofs":["deterministic-run","boundary-validation"],**boundary_fields()}
