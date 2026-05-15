REGULATED_FLAGS=["financial advice","investment advice","payment/custody","wallet/trading","KYC/AML","legal advice","medical advice","HR/worker evaluation","credit/lending","insurance","critical-infrastructure control","energy/utility markets","biometric identification","emotion recognition","law enforcement","migration/border","education scoring","justice/democratic process","offensive cyber"]

def _normalize(s:str)->str:
    return ' '.join(
        s.lower()
        .replace('/', ' ')
        .replace('-', ' ')
        .split()
    )

def regulated_boundary_triage(workflow:dict)->dict:
    t=_normalize(workflow.get('workflow_type','')+' '+workflow.get('description',''))
    hits=[f for f in REGULATED_FLAGS if _normalize(f) in t]
    blocked=bool(hits)
    return {
        'regulated_flags_triggered':hits,
        'regulated_boundary_blocked':blocked,
        'status':'blocked_human_review_required' if blocked else 'documentation_only',
        'safe_explanation':'No automated execution for regulated domains.' if blocked else 'Synthetic non-regulated workflow.'
    }
