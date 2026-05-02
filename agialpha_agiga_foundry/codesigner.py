def codesign(n):
    n["codesign"]={"task":n["task_manifest"],"solver":n["solver_spec"],"validator":n["validator_spec"],"evidence":n["evidence_docket_template"],"replay_plan":"deterministic"}
    return n
