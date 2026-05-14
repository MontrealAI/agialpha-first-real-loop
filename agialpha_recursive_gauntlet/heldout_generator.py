from .context import *
FAMS=["Missing Evidence Docket repair","Shallow experiment page repair","Workflow catalog missing entry","Broken launchpad workflow link","Missing safety ledger","Missing claim boundary","Unsafe positive overclaim","Token investment overclaim","Auto-merge pattern","Missing ProofBundle hash","Missing replay instructions","Missing human review record","Missing Work Vault link","Missing MARK allocation","Missing Sovereign assignment","vNext candidate with no validator"]
def generate_heldout(run: Path, task_count:int=16):
    lock=run/'03_candidate_lock/candidate_lock.json'
    if not lock.exists(): raise SystemExit('candidate lock required before heldout generation')
    tasks=[]
    for i in range(task_count):
        fam=FAMS[i%len(FAMS)]
        tasks.append({"task_id":f"task-{i+1:03d}","task_family":fam,"input_fixture":{"id":i},"expected_behavior":"repair and preserve claim boundary","validator":"static_validator","claim_boundary":CLAIM_BOUNDARY,"safety_requirements":["no automerge","no external scan"]})
    write_json(run/'04_heldout_tasks/heldout_tasks.json',{"generated_at":now_iso(),"claim_boundary":CLAIM_BOUNDARY,"tasks":tasks})
    return tasks
