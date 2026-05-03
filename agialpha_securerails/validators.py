import json
def validate_vault(v):
 return v["hard_safety_counters"]["external_target_scan_count"]==0 and v.get("claim_boundary")
