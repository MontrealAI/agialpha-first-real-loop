MINIMUM_ADVANTAGE_DELTA = 0.15
ALLOWED_ECI = {"E3_REPLAYED", "E4_STRESS_TESTED", "E5_EXTERNALLY_VALIDATED"}

def promotion_gate(delta, eci, minimum_advantage_delta=MINIMUM_ADVANTAGE_DELTA):
    return delta >= minimum_advantage_delta and eci in ALLOWED_ECI
