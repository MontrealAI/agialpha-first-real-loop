from .boundaries import boundary_fields
def create_docket(pilot_id:str,proofbundle_id:str)->dict:
 return {"evidence_docket_id":f"docket-{pilot_id}","pilot_id":pilot_id,"proofbundle_id":proofbundle_id,"status":"generated",**boundary_fields()}
