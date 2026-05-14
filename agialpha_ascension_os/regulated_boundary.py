REGULATED_FLAGS=["financial advice","investment advice","payment/custody","wallet/trading","KYC/AML","legal advice","medical advice","HR/worker evaluation","credit/lending","insurance","critical-infrastructure control","energy/utility markets","biometric identification","emotion recognition","law enforcement","migration/border","education scoring","justice/democratic process","offensive cyber"]

def regulated_boundary_triage(workflow:dict)->dict:
    t=(workflow.get('workflow_type','')+' '+workflow.get('description','')).lower()
    hits=[f for f in REGULATED_FLAGS if f.lower().split('/')[0] in t]
    blocked=bool(hits)
    return {
        'regulated_flags_triggered':hits,
        'regulated_boundary_blocked':blocked,
        'status':'blocked_human_review_required' if blocked else 'documentation_only',
        'safe_explanation':'No automated execution for regulated domains.' if blocked else 'Synthetic non-regulated workflow.'
    }
