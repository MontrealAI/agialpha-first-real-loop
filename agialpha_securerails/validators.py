from .safety import HARD_COUNTERS

def validate_vault(v):
    counters = v.get("hard_safety_counters", {})
    if not v.get("claim_boundary"):
        return False
    for key in HARD_COUNTERS:
        if key not in counters:
            return False
        if counters[key] != 0:
            return False
    return True
