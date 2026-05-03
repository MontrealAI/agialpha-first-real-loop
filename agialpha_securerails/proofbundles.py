import json,os
def make_proofbundle(out_dir,vault):
 o={"proofbundle_id":"proofbundle-demo-001","vault_id":vault["vault_id"],"replay_status":"replayable"};json.dump(o,open(os.path.join(out_dir,"proofbundle.json"),"w"),indent=2);return o
