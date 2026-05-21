from __future__ import annotations

from .context import BOUNDARIES


def base_record(extra=None):
    rec={**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True})
    return rec

__doc__ = "Failure learning package helpers."

def build_failure_learning(job_id:str, reason:str):
    return {"failure_learning_id":f"fl-{job_id}","source_job_id":job_id,"reason":reason,**base_record()}
