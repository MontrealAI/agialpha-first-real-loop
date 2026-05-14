from .context import BOUNDARY
def build():
 axes=[]
 for i,n in enumerate(range(1,26),1): axes.append({"axis_id":f"axis-{i:02d}","axis_name":f"Axis {i}","score":"not_reported","max_score":100,"evidence_level":"local","evidence_links":[],"supporting_artifacts":[],"missing_evidence":[],"next_best_action":"collect more evidence",**BOUNDARY})
 return {"axes":axes,**BOUNDARY}
