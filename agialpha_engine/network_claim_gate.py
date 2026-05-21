from __future__ import annotations

from .context import BOUNDARIES


def base_record(extra=None):
    rec={**BOUNDARIES,"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True}
    if extra: rec.update(extra)
    return rec

__doc__ = "Network claim gate evaluation."

def supported_status(ok:bool)->str:
    return "supported_local_bounded" if ok else "not_supported"
