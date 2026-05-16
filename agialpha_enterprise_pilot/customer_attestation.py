from .boundaries import EXCLUDED_USES,envelope
def build_attestation(pilot_id): d={'pilot_id':pilot_id,'excluded_uses':EXCLUDED_USES,'excluded_uses_acknowledged':True}; d.update(envelope()); return d
