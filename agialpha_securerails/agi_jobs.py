import json,os
def run_job(out_dir,vault):
 o={"job_id":"job-demo-001","vault_id":vault["vault_id"],"status":"completed","task":"workflow permission review"};json.dump(o,open(os.path.join(out_dir,"agi-job.json"),"w"),indent=2);return o
