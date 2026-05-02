SEED_TYPES=["task","validator","solver","workflow","evidence","replay","safety","cost","runbook","capability","descendant","kernel_mutation"]

def opportunity_to_nova_seeds(opportunity:dict):
    out=[]
    for i,seed_type in enumerate(SEED_TYPES):
        out.append({
            "schema_version":"agialpha.agiga.nova_seed.v1",
            "nova_seed_id":f"{opportunity['opportunity_id']}-seed-{i:02d}",
            "parent_opportunity_id":opportunity['opportunity_id'],
            "seed_type":seed_type,
            "variant_family":opportunity.get('domain','general'),
            "seed_payload":{"hint":opportunity.get('descendant_niche_hint','')},
            "expected_benefit":"validated work capacity",
            "risk_tier":"medium",
            "proof_requirement":"validator+replay+falsification",
            "mutation_operators":["local_perturb"],
            "claim_boundary":opportunity.get('claim_boundary','')
        })
    return out
