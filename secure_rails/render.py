from __future__ import annotations
import json, html
from pathlib import Path
CLAIM="SecureRails is AI-agent security governance and proof-bound defensive remediation. It is not autonomous cybersecurity certification, not offensive cyber, not a high-risk decision system by intended purpose, not a GPAI model provider by default, and not an investment product."

def _j(path: Path): return json.loads(path.read_text(encoding='utf-8')) if path.exists() else []

def build_data(registry: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    w,m,s,st=[_j(registry/f) for f in ('work_vaults.json','mark_allocations.json','sovereigns.json','settlements.json')]
    for n,v in [('work_vaults.json',w),('mark_allocations.json',m),('sovereigns.json',s),('settlements.json',st)]:
        (out/n).write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
    summary={"generated_at":"1970-01-01T00:00:00Z","work_vault_count":len(w),"open_vault_count":sum(1 for x in w if x.get('status')=='vault_opened' or x.get('status')=='example_not_production'),"accepted_vault_count":sum(1 for x in w if x.get('status')=='accepted'),"rejected_vault_count":sum(1 for x in w if x.get('status')=='rejected'),"pending_human_review_count":sum(1 for x in w if x.get('evidence',{}).get('human_review_status') in ('pending','not_reported')),"all_hard_safety_counters_zero":all(all((x.get('hard_safety_counters',{}).get(k,0)==0) for k in ['raw_secret_leak_count','external_target_scan_count','exploit_execution_count','malware_generation_count','social_engineering_content_count','unsafe_automerge_count','critical_safety_incidents']) for x in w),"sovereign_count":len(s),"mark_allocation_count":len(m),"settlement_record_count":len(st),"claim_boundary":CLAIM}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")

def render_html(registry: Path, out: Path) -> None:
    d = out / '_data'
    build_data(registry, d)
    w=_j(d/'work_vaults.json'); m=_j(d/'mark_allocations.json'); s=_j(d/'sovereigns.json'); st=_j(d/'settlements.json'); sm=_j(d/'summary.json')
    out.mkdir(parents=True, exist_ok=True)
    chain='AI-agent work event → Work Vault → MARK → Sovereign → AGI Job → ProofBundle → Evidence Docket → Human Review → $AGIALPHA Utility Settlement → Capability Archive → vNext Defensive Work'
    body=f"<h1>SecureRails Work Vaults</h1><p>Proof, safety, review, and $AGIALPHA utility settlement containers for AI-agent security governance and proof-bound defensive remediation.</p><p>{chain}</p><h2>Status</h2><pre>{html.escape(json.dumps(sm,indent=2))}</pre><h2>Claim boundary</h2><p>{html.escape(CLAIM)}</p><h2>Human review required</h2><p>true</p><h2>No auto-merge posture</h2><p>auto_merge_allowed: false</p>"
    (out/'index.html').write_text('<!doctype html><meta charset="utf-8">'+body, encoding='utf-8')
