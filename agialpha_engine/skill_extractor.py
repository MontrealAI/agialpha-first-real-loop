from __future__ import annotations

from .context import BOUNDARIES


def base_record(extra=None):
    rec={**BOUNDARIES,"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True}
    if extra: rec.update(extra)
    return rec

__doc__ = "Deterministic skill extraction routing."

def classify_job(job_index:int)->str:
    return ["accepted","rejected","failure"][job_index%3]
