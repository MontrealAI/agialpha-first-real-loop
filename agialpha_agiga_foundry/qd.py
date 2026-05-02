def build_qd(niches): return [{"niche_id":n["niche_id"],"descriptor":n["family"],"status":n.get("status","candidate")} for n in niches]
