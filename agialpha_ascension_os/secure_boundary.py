from .context import BOUNDARY,SAFETY_COUNTERS
def check(): return {"status":"pass","hard_safety_counters":SAFETY_COUNTERS,**BOUNDARY}
