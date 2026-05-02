def allocate_mark(nova_seed:dict)->dict:
    return {
        "schema_version":"agialpha.agiga.mark_allocation.v1",
        "allocation_id":f"alloc-{nova_seed['nova_seed_id']}",
        "nova_seed_id":nova_seed['nova_seed_id'],
        "allocated_budget_proxy":1,
        "review_priority":"high" if nova_seed['seed_type'] in {'validator','kernel_mutation'} else "medium",
        "risk_tier":nova_seed.get('risk_tier','medium'),
        "validator_required":True,
        "replay_required":True,
        "falsification_required":True,
        "human_review_required_for_promotion":True,
        "promotion_threshold":{"min_advantage_delta":0.15},
        "rejection_reason_if_any":""
    }
