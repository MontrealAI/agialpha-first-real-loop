from __future__ import annotations

from .context import BOUNDARIES


def base_record(extra=None):
    rec={**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True})
    return rec

__doc__ = "Held-out propagation comparison helpers."

def network_skill_propagation_lift(d_shared:float,d_base:float)->float:
    return round(float(d_shared)-float(d_base),6)
