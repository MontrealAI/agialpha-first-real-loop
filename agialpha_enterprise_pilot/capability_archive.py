from .boundaries import boundary_fields

def create_capability_archive_entry(pilot_id: str):
    return {"pilot_id": pilot_id, "status": "archived", **boundary_fields()}
