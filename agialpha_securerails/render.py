import os,json
from .safety import HARD_COUNTERS

def _safety_status(run_dir):
    ledger_path=os.path.join(run_dir,'safety-ledger.json')
    counters=json.load(open(ledger_path)) if os.path.exists(ledger_path) else {}
    missing=[k for k in HARD_COUNTERS if k not in counters]
    nonzero={k:v for k,v in counters.items() if k in HARD_COUNTERS and v!=0}
    if missing:
        return f"incomplete ({len(missing)} missing counters)"
    if nonzero:
        return f"violations ({len(nonzero)} non-zero counters)"
    return "clean"

def render(run_dir,out_dir):
 os.makedirs(out_dir,exist_ok=True)
 v=json.load(open(os.path.join(run_dir,'work-vault.json')));m=json.load(open(os.path.join(run_dir,'mark-allocation.json')));s=json.load(open(os.path.join(run_dir,'settlement-receipt.json')))
 safety_status=_safety_status(run_dir)
 html=f"""# SecureRails Work Vaults

- Vault ID: {v['vault_id']}
- Status: {v['status']}
- Assigned Sovereign: {v['assigned_sovereign']}
- MARK allocation: {m['allocation_id']}
- Risk tier: {m['risk_tier']}
- Replay status: replayable
- Safety status: {safety_status}
- Human review status: required
- Safe PR status: not merged
- $AGIALPHA utility budget: {m['allocated_budget_proxy']}
- Settlement status: {s['status']}
- Capability archived: yes
- vNext reuse status: queued

No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.
"""
 open(os.path.join(out_dir,'README.md'),'w').write(html)
