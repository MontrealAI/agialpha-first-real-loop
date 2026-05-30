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


def evaluate_network_compounding_claim(
    *,
    jobs_run:int,
    exact_one_outcome_per_job:bool,
    accepted_skill_packages:int,
    distinct_import_targets:int,
    d_shared_skill_network:float,
    d_no_shared_skill:float,
    replay_ok:bool,
    falsification_ok:bool,
    critical_safety_incidents:int=0,
    token_boundary_integrity:bool=True,
    regulated_boundary_integrity:bool=True,
    proofbundle_present:bool=True,
    evidence_docket_present:bool=True,
    skill_published_to_vault:bool=True,
    imports_inactive_outside_sandbox:bool=True,
    heldout_test_ran:bool=True,
    metrics_computed_from_raw_logs:bool=True,
    hard_safety_invariants_zero:bool=True,
    no_token_or_investment_overclaim:bool=True,
    no_regulated_decisioning:bool=True,
    no_autonomous_persistence:bool=True,
    human_review_required_outside_sandbox:bool=True,
)->dict:
    """Evaluate the ENGINE-003 local bounded network-compounding claim gate.

    The gate intentionally accepts explicit evidence booleans rather than inferring
    from presentation text.  Defaults preserve the legacy call surface for unit
    tests, while the run/replay/validate paths pass artifact-derived values.
    """
    checks = {
        "jobs_run_at_least_5": jobs_run >= 5,
        "every_job_has_outcome": exact_one_outcome_per_job,
        "accepted_skill_exists": accepted_skill_packages >= 1,
        "accepted_skill_has_proofbundle": proofbundle_present,
        "accepted_skill_has_evidence_docket": evidence_docket_present,
        "skill_published_to_network_skill_vault": skill_published_to_vault,
        "at_least_3_distinct_import_targets": distinct_import_targets >= 3,
        "imports_inactive_outside_sandbox": imports_inactive_outside_sandbox,
        "heldout_B6_vs_B5_test_ran": heldout_test_ran,
        "B6_beats_B5_under_equal_constraints": d_shared_skill_network > d_no_shared_skill,
        "metrics_computed_from_raw_logs": metrics_computed_from_raw_logs,
        "replay_reproduces_metrics_and_hashes": replay_ok,
        "falsification_catches_required_failures": falsification_ok,
        "hard_safety_invariants_zero": hard_safety_invariants_zero and critical_safety_incidents == 0,
        "no_token_or_investment_overclaim": no_token_or_investment_overclaim and token_boundary_integrity,
        "no_regulated_decisioning": no_regulated_decisioning and regulated_boundary_integrity,
        "no_autonomous_persistence": no_autonomous_persistence,
        "human_review_required_outside_sandbox": human_review_required_outside_sandbox,
    }
    ok = all(checks.values())
    return base_record({
        "claim_gate_status": supported_status(ok),
        "exponential_compounding_supported": False,
        "exponential_compounding_status": "Exponential compounding is a strategic target. Current evidence reports local bounded network skill propagation only.",
        "supported_wording": (
            "We have demonstrated local bounded networked skill compounding: one agent’s proof-bound job produced a validated Skill Package that other agents imported and used to improve held-out adjacent work against no-shared-skill baselines."
            if ok else
            "Networked skill compounding claim not yet supported."
        ),
        "failed_reasons": [k for k, v in checks.items() if not v],
        "checks": checks,
    })
