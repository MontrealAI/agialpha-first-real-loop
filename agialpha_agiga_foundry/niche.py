import copy
def make_niche(i,family,opp):
    return {"niche_id":f"niche-{i:03d}","family":family,"opportunity_intermediate":opp,"challenge_statement":f"Solve {family}","task_manifest":{"task":"bounded"},"solver_spec":{"strategy":"deterministic"},"validator_spec":{"type":"threshold"},"baseline_spec":{"baseline":"B5"},"safety_policy":{},"replay_instructions":"cli replay","cost_ledger_template":{},"evidence_docket_template":{},"success_criteria":{"score_gte":0.6},"risk_tier":"low","claim_boundary":"bounded local/proxy evidence only","useful_capacity_hypothesis":"increase validated work","local_mutation_operators":["task"],"descendant_niche_hints":["harder"]}
def mutate_niche(n,vid):m=copy.deepcopy(n);m['variant_id']=vid;return m
