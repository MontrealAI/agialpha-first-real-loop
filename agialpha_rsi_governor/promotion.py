def promotion_gate(delta, eci): return delta > 0 and eci in {"E3_REPLAYED","E4_STRESS_TESTED","E5_EXTERNALLY_VALIDATED"}
