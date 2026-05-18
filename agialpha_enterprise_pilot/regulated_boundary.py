from .boundaries import boundary_fields
import re
BANNED=["hr","human resources","worker evaluation","credit","lending","loan","insurance","medical","legal","kyc","aml","custody","payment","banking","brokerage","procurement","contract","investment","financial advice","securities","trading"]
def triage(intake:dict)->dict:
 raw=(intake.get("intended_use","")+" "+intake.get("workflow_family","")+" "+intake.get("domain","")).lower()
 t=re.sub(r"[^a-z0-9]+"," ",raw).strip(); blocked=any(re.search(rf"\b{re.escape(b)}\b", t) for b in BANNED)
 pilot_id=intake.get("pilot_id","not_reported")
 return {"triage_id":f"triage-{pilot_id}","pilot_id":pilot_id,"regulated_boundary_blocked":blocked,"status":"blocked" if blocked else "passed","block_reason":"regulated_boundary_blocked" if blocked else "none",**boundary_fields()}
