from .boundaries import boundary_fields

def create_pilot_scope(pilot_id: str):
    return {"pilot_id": pilot_id, "scope": "synthetic_fixture_only", **boundary_fields()}
