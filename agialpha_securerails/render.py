import os,json
def render(run_dir,out_dir):
 os.makedirs(out_dir,exist_ok=True)
 v=json.load(open(os.path.join(run_dir,'work-vault.json')));m=json.load(open(os.path.join(run_dir,'mark-allocation.json')));s=json.load(open(os.path.join(run_dir,'settlement-receipt.json')))
 html=f"""# SecureRails Work Vaults

- Vault ID: {v['vault_id']}
- Status: {v['status']}
- Assigned Sovereign: {v['assigned_sovereign']}
- MARK allocation: {m['allocation_id']}
- Risk tier: {m['risk_tier']}
- Replay status: replayable
- Safety status: clean
- Human review status: required
- Safe PR status: not merged
- $AGIALPHA utility budget: {m['allocated_budget_proxy']}
- Settlement status: {s['status']}
- Capability archived: yes
- vNext reuse status: queued

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
"""
 open(os.path.join(out_dir,'README.md'),'w').write(html)
