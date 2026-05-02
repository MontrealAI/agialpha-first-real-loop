def novelty(n): return (len(n["niche_id"])%10)/10
def diversity(niches): return len(set(n["family"] for n in niches))/max(1,len(niches))
