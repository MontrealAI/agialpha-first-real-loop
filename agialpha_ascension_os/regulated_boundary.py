import re

REGULATED_FLAGS=["financial advice","investment advice","payment/custody","wallet/trading","KYC/AML","legal advice","medical advice","HR/worker evaluation","credit/lending","insurance","critical-infrastructure control","energy/utility markets","biometric identification","emotion recognition","law enforcement","migration/border","education scoring","justice/democratic process","offensive cyber"]


def _matches_flag(text: str, flag: str) -> bool:
    """Match regulated phrases; slash-delimited terms are OR-keyword triggers."""
    if "/" in flag:
        terms = [part.strip().lower() for part in flag.split("/") if part.strip()]
        return any(bool(re.search(rf"\b{re.escape(term)}\b", text)) for term in terms)
    candidate = re.sub(r"[-]+", " ", flag.lower())
    candidate = re.sub(r"\s+", " ", candidate).strip()
    pattern = rf"\b{re.escape(candidate)}\b"
    return bool(re.search(pattern, text))

def regulated_boundary_triage(workflow:dict)->dict:
    t=(workflow.get('workflow_type','')+' '+workflow.get('description','')).lower()
    normalized_text = re.sub(r"[-]+", " ", t)
    normalized_text = re.sub(r"\s+", " ", normalized_text).strip()
    hits=[f for f in REGULATED_FLAGS if _matches_flag(normalized_text, f)]
    blocked=bool(hits)
    return {
        'regulated_flags_triggered':hits,
        'regulated_boundary_blocked':blocked,
        'status':'blocked_human_review_required' if blocked else 'documentation_only',
        'safe_explanation':'No automated execution for regulated domains.' if blocked else 'Synthetic non-regulated workflow.'
    }
