from .boundaries import boundary_fields
def render_outcome_md(pilot_id:str,tier:str)->str:
 return f"# Pilot Outcome Dossier\n\nPilot: {pilot_id}\n\nCommercial readiness: {tier}\n\nHuman review required: true\n"
