import copy
def generate_candidates(kernel, n):
    out=[]
    for i in range(1,n+1):
        c=copy.deepcopy(kernel); c["candidate_id"]=f"candidate-{i:03d}"; c["kernel_version"]=f"0.1.{i}"; c["mutation_rationale"]="adjust completeness weight"; c["changed_fields"]=["scoring_weights.page_completeness"]; c["expected_benefit"]="improved completeness"; c["expected_risk"]="false positives"; c["rollback_note"]="restore baseline"; c["claim_boundary_impact"]="none"; c["safety_impact"]="none"; out.append(c)
    return out
