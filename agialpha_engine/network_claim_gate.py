from __future__ import annotations

from .context import BOUNDARIES


def base_record(extra=None):
    rec={**BOUNDARIES}
    if extra:
        rec.update(extra)
    rec.update({"human_review_required":True,"autonomous_persistence_allowed":False,"no_auto_merge":True})
    return rec

__doc__ = "Network claim gate evaluation."

def supported_status(ok:bool)->str:
    return "supported_local_bounded" if ok else "not_supported"


def evaluate_network_compounding_claim(*, jobs_run:int, exact_one_outcome_per_job:bool, accepted_skill_packages:int, distinct_import_targets:int, d_shared_skill_network:float, d_no_shared_skill:float, replay_ok:bool, falsification_ok:bool, critical_safety_incidents:int=0, token_boundary_integrity:bool=True, regulated_boundary_integrity:bool=True)->dict:
    checks = {
        "jobs_run_at_least_5": jobs_run >= 5,
        "every_job_has_outcome": exact_one_outcome_per_job,
        "accepted_skill_exists": accepted_skill_packages >= 1,
        "at_least_3_distinct_import_targets": distinct_import_targets >= 3,
        "B6_beats_B5": d_shared_skill_network > d_no_shared_skill,
        "replay_ok": replay_ok,
        "falsification_ok": falsification_ok,
        "critical_safety_incidents_zero": critical_safety_incidents == 0,
        "token_boundary_integrity": token_boundary_integrity,
        "regulated_boundary_integrity": regulated_boundary_integrity,
    }
    ok = all(checks.values())
    return base_record({
        "claim_gate_status": supported_status(ok),
        "exponential_compounding_status": "Exponential compounding is a strategic target. Current evidence reports local bounded network skill propagation only.",
        "supported_wording": (
            "We have demonstrated local bounded networked skill compounding: one agent’s proof-bound job produced a validated Skill Package that other agents imported and used to improve held-out adjacent work against no-shared-skill baselines."
            if ok else
            "Networked skill compounding claim not yet supported."
        ),
        "failed_reasons": [k for k, v in checks.items() if not v],
        "checks": checks,
    })
