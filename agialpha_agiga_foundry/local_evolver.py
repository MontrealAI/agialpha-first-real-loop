from .niche import mutate_niche
def evolve(n,k):
    vs=[mutate_niche(n,f"v{i+1}") for i in range(k)]
    if not vs:
        return {"variants": [], "winner": None, "rejected": [], "error": "no_local_variants_configured"}
    return {"variants":vs,"winner":vs[0],"rejected":vs[1:]}
