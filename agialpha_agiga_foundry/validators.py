def validate_niche(n): return all(k in n for k in ["task_manifest","solver_spec","validator_spec","claim_boundary"])
def run_validator(n):
    s=(len(n["family"])%10)/10
    return {"score":s,"pass":s>=n["success_criteria"]["score_gte"]}
