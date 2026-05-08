def scorecard_status(enabled=False):
    return {"enabled": enabled, "status": "not_run" if not enabled else "unavailable"}
