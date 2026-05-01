def apply(policy: dict, context: dict|None=None) -> dict:
    return {"policy": "falsification", "status": "ok", "human_review_required": policy.get("human_review_required", True)}
