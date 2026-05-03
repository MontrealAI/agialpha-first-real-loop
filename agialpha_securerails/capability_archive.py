import json,os
def make_archive(out_dir,vault):
 o={"schema_version":"1.0.0","entry_id":"capability-demo-001","vault_id":vault["vault_id"],"capability":"workflow permission defensive review","vnext_reuse_status":"queued"};json.dump(o,open(os.path.join(out_dir,"capability-archive-entry.json"),"w"),indent=2);return o
