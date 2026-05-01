def d_governance(m):
    num = m["page_completeness_score"]*m["evidence_integrity_score"]*m["replay_readiness_score"]*m["claim_boundary_integrity"]*m["safety_integrity"]*m["workflow_launchability"]*m["registry_persistence_score"]*m["future_work_recommendation_score"]*m["human_review_gate_integrity"]
    return num/(1+m.get("coordination_overhead",0)+m.get("false_positive_penalty",0)+m.get("false_negative_penalty",0))
