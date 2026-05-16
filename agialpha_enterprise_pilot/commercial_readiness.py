from .boundaries import boundary_fields

def build_scorecard(has_attestation=True,has_triage=True,has_proofbundle=True,has_docket=True,has_replay=True,has_review=True,repeatable=True,paid=False):
 tier='C0'
 if True: tier='C1'
 if has_attestation and has_triage: tier='C2'
 if has_proofbundle and has_docket: tier='C4'
 if has_replay: tier='C5'
 if has_review: tier='C6'
 if repeatable: tier='C7'
 if not paid and tier>'C8': tier='C8'
 if not has_attestation or not has_triage: tier=min(tier,'C1')
 if (not has_docket) or (not has_proofbundle): tier=min(tier,'C3')
 if not has_replay: tier=min(tier,'C4')
 if not has_review: tier=min(tier,'C5')
 if not repeatable: tier=min(tier,'C6')
 return {"commercial_readiness_tier":tier,"paid_pilot_or_commercial_commitment_status":"not_reported" if not paid else "redacted_present","missing_evidence":["paid_pilot_or_commercial_commitment_status:not_reported"] if not paid else [],**boundary_fields()}
