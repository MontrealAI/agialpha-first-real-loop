import json
from datetime import datetime, timezone
from pathlib import Path

def build_customer_pilot_data(registry: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    records=json.loads((registry/'registry.json').read_text(encoding='utf-8')).get('records',[])
    summary={"generated_at":datetime.now(timezone.utc).isoformat(),"pilot_count":len(records),"validated_pilot_count":sum(r.get('status')=='validated' for r in records),"quarantined_pilot_count":sum(r.get('status')=='quarantined' for r in records),"public_display_count":sum(r.get('privacy',{}).get('public_display_allowed') is True for r in records),"private_only_count":sum(r.get('privacy',{}).get('public_display_allowed') is not True for r in records),"all_hard_safety_counters_zero":all(not any((r.get('hard_safety_counters') or {}).values()) for r in records),"human_review_pending_count":sum(r.get('evidence',{}).get('human_review_status')=='pending' for r in records),"artifact_expired_count":sum(r.get('source',{}).get('artifact_status')=='expired' for r in records),"claim_boundary":"SecureRails customer pilot summaries are evidence-governance only."}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (out/'pilot_runs.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    (out/'repos.json').write_text(json.dumps(sorted({f"{r['repo']['owner']}/{r['repo']['name']}" for r in records if r.get('repo')}),indent=2),encoding='utf-8')
    latest=records[-1] if records else {}
    (out/'latest.json').write_text(json.dumps(latest,indent=2),encoding='utf-8')
