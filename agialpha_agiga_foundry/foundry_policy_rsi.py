"""FoundryPolicy RSI evaluation facade."""

def foundry_policy_improvement(candidate_score: float, incumbent_score: float) -> float:
    """Return policy advantage delta for held-out policy tasks."""
    return candidate_score - incumbent_score
