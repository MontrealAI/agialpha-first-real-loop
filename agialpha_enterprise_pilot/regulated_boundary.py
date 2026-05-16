from .boundaries import boundary_fields
BANNED=["hr","credit","insurance","medical","legal","kyc","aml","custody","payment","brokerage","procurement","contract"]
def triage(intake:dict)->dict:
 t=(intake.get("intended_use","")+" "+intake.get("workflow_family","")).lower(); blocked=any(b in t for b in BANNED)
 return {"triage_id":f"triage-{intake['pilot_id']}","pilot_id":intake['pilot_id'],"regulated_boundary_blocked":blocked,"status":"blocked" if blocked else "passed","block_reason":"regulated_boundary_blocked" if blocked else "none",**boundary_fields()}
