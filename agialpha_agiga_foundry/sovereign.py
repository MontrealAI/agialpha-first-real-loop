def form_sovereign(opportunity:dict,nova_seeds:list)->dict:
    return {
        "schema_version":"agialpha.agiga.sovereign.v1",
        "sovereign_id":f"sovereign-{opportunity['opportunity_id']}",
        "sovereign_name":f"{opportunity.get('domain','General').title()} Sovereign",
        "formed_from_opportunity_id":opportunity['opportunity_id'],
        "formed_from_nova_seeds":[s['nova_seed_id'] for s in nova_seeds],
        "domain":opportunity.get('domain','general'),
        "task_family":opportunity.get('domain','general'),
        "validators":["default_validator"],
        "proofbundle_policy":{"required":True},
        "evidence_docket_policy":{"required":True},
        "archive_policy":{"append_only":True},
        "promotion_policy":{"human_review_required":True},
        "claim_boundary":opportunity.get('claim_boundary','')
    }
