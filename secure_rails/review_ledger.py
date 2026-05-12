import json
from pathlib import Path
from datetime import datetime, timezone
from .review_request import validate_review_request
from .review_decision import validate_review_decision
from .human_review import validate_promotion_gate

def _now(): return datetime.now(timezone.utc).isoformat()

def ensure_registry(registry: Path):
    (registry/'requests').mkdir(parents=True, exist_ok=True)
    (registry/'decisions').mkdir(parents=True, exist_ok=True)
    (registry/'promotion_gates').mkdir(parents=True, exist_ok=True)
    (registry/'indexes').mkdir(parents=True, exist_ok=True)
    if not (registry/'registry.json').exists(): (registry/'registry.json').write_text(json.dumps({"entries":[]},indent=2),encoding='utf-8')

def _decision_exists(registry: Path, decision_id: str) -> bool:
    return (registry / 'decisions' / f'{decision_id}.json').exists()

def update_ledger(input_path: Path, registry: Path):
    ensure_registry(registry)
    rec=json.loads(input_path.read_text(encoding='utf-8'))
    if rec.get('schema_version')=='securerails.human_review_request.v1':
        errs=validate_review_request(rec); kind='request'; rid=rec.get('review_request_id','unknown'); out=registry/'requests'/f'{rid}.json'
    elif rec.get('schema_version')=='securerails.human_review_decision.v1':
        errs=validate_review_decision(rec); kind='decision'; rid=rec.get('decision_id','unknown'); out=registry/'decisions'/f'{rid}.json'
    elif rec.get('schema_version')=='securerails.promotion_gate.v1':
        errs=validate_promotion_gate(rec); kind='promotion_gate'; rid=rec.get('promotion_gate_id','unknown'); out=registry/'promotion_gates'/f'{rid}.json'
        source_decision_id = rec.get('source_decision_id', '')
        if not source_decision_id:
            errs.append('source_decision_id required')
        elif not _decision_exists(registry, source_decision_id):
            errs.append('source_decision_id not found in registry decisions')
    else: raise ValueError('unsupported schema_version')
    if errs: raise ValueError('; '.join(errs))
    out.write_text(json.dumps(rec,indent=2),encoding='utf-8')
    reg=json.loads((registry/'registry.json').read_text())
    reg['entries'].append({'id':rid,'kind':kind,'path':str(out.relative_to(registry)),'updated_at':_now()})
    (registry/'registry.json').write_text(json.dumps(reg,indent=2),encoding='utf-8')
    (registry/'latest.json').write_text(json.dumps({'latest':reg['entries'][-1]},indent=2),encoding='utf-8')

def validate_ledger(registry: Path)->list[str]:
    errs=[]
    if not (registry/'registry.json').exists(): errs.append('missing registry.json')
    return errs
