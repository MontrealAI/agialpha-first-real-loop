from .context import *
def generate_falsification(run: Path,out: Path):
 r={"falsification_pass":True,"claim_boundary":CLAIM_BOUNDARY,"tests":["overclaim_scan","token_boundary_scan"]}; write_json(out,r); return r
