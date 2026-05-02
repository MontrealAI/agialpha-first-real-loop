from .niche import mutate_niche
def evolve(n,k):
    vs=[mutate_niche(n,f"v{i+1}") for i in range(k)]
    return {"variants":vs,"winner":vs[0],"rejected":vs[1:]}
