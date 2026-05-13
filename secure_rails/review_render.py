import json
from pathlib import Path

def build_data(registry: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    req=[json.loads(p.read_text()) for p in sorted((registry/'requests').glob('*.json'))]
    dec=[json.loads(p.read_text()) for p in sorted((registry/'decisions').glob('*.json'))]
    gates=[json.loads(p.read_text()) for p in sorted((registry/'promotion_gates').glob('*.json'))]
    request_ids={r.get('review_request_id') for r in req if isinstance(r.get('review_request_id'), str) and r.get('review_request_id').strip()}
    decided_request_ids={d.get('review_request_id') for d in dec if isinstance(d.get('review_request_id'), str) and d.get('review_request_id').strip()}
    summary={"pending_reviews":len(request_ids - decided_request_ids),"accepted_decisions":sum(1 for d in dec if d.get('decision')=='accept'),"rejected_decisions":sum(1 for d in dec if d.get('decision')=='reject'),"escalated_decisions":sum(1 for d in dec if d.get('decision')=='escalate'),"requests_for_changes":sum(1 for d in dec if d.get('decision')=='request_changes'),"archive_only_decisions":sum(1 for d in dec if d.get('decision')=='archive_only'),"promotion_gates_passed":sum(1 for g in gates if g.get('gate_status')=='pass'),"promotion_gates_failed":sum(1 for g in gates if g.get('gate_status')=='fail')}
    (out/'requests.json').write_text(json.dumps(req,indent=2),encoding='utf-8')
    (out/'decisions.json').write_text(json.dumps(dec,indent=2),encoding='utf-8')
    (out/'promotion_gates.json').write_text(json.dumps(gates,indent=2),encoding='utf-8')
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    latest={"request":req[-1] if req else None,"decision":dec[-1] if dec else None,"promotion_gate":gates[-1] if gates else None}
    (out/'latest.json').write_text(json.dumps(latest,indent=2),encoding='utf-8')
