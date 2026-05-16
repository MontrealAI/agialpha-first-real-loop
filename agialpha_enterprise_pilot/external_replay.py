from .boundaries import boundary_fields
def create_external_replay(pilot_id:str)->dict:
 return {"external_replay_packet_id":f"replay-{pilot_id}","pilot_id":pilot_id,"status":"generated",**boundary_fields()}
