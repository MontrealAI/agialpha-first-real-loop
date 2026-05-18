from .context import BOUNDARIES
FAMILIES=["docs usability repair","workflow catalog completeness","Evidence Docket completeness","ProofBundle completeness","generated-data index health","broken-link repair","claim-boundary hardening","token-boundary hardening","regulated-boundary hardening","SecureRails safety-ledger hardening","no-auto-merge enforcement","replay determinism repair","falsification audit hardening","schema validation repair","benchmark adapter readiness","Open RSI Eval fixture generation","Self-Improvement Gauntlet fixture generation","QD archive coverage","capability archive compression","lineage metaproductivity measurement","enterprise pilot readiness","valuation-support missing-evidence repair","public UI card completeness","operator runbook quality","reviewer replay kit quality","Work Vault accounting integrity","utility receipt boundary","MARK/Sovereign linkage","rejected-variant preservation","vNext descendant generation","negative-result ledger","external replay readiness"]
def generate_tasks(n):
    tasks=[]
    for i in range(n):
        fam=FAMILIES[i%len(FAMILIES)]
        t={"schema_version":"agialpha.engine.task.v1","task_id":f"ENG-TASK-{i+1:03d}","family":fam,"title":f"{fam} task {i+1}","opportunity":"repo-owned deterministic improvement","repo_owned_scope":True,"synthetic_fixture_only":True,"regulated_domain_flags":{"regulated":False},"allowed_mode":"safe_local_eval","task_manifest":{"target":"docs"},"validator_spec":{"type":"presence_check"},"solver_plan":{"type":"patch_proposal_only"},"success_criteria":["validator_pass"],"baseline_plan":{"compare":["B5","B6"]},"ablation_plan":{"variants":["no_archive","full_engine"]},"replay_plan":{"deterministic":True},"evidence_docket_plan":{"required":True},"risk_tier":"low"}
        t.update(BOUNDARIES)
        tasks.append(t)
    return tasks
