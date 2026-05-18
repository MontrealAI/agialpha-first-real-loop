from .boundaries import boundary_fields
def create_customer_review(pilot_id:str)->dict:
 return {"customer_review_id":f"review-{pilot_id}","pilot_id":pilot_id,"status":"pending","decision":"pending",**boundary_fields()}
