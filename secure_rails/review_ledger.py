import json
import re
from pathlib import Path
from datetime import datetime, timezone
from .review_request import validate_review_request
from .review_decision import validate_review_decision
from .human_review import validate_promotion_gate

def _now(): return datetime.now(timezone.utc).isoformat()
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")

def _safe_out_path(registry: Path, folder: str, rid: str) -> Path:
    if not isinstance(rid, str) or not SAFE_ID_RE.fullmatch(rid):
        raise ValueError(f"unsafe id: {rid!r}")
    out = (registry / folder / f"{rid}.json").resolve()
    reg_root = registry.resolve()
    if reg_root not in out.parents:
        raise ValueError("output path escapes registry")
    return out

def _required_id(rec: dict, key: str) -> str:
    rid = rec.get(key)
    if not isinstance(rid, str) or not rid.strip():
        raise ValueError(f"missing required id: {key}")
    return rid

def ensure_registry(registry: Path):
    (registry/'requests').mkdir(parents=True, exist_ok=True)
    (registry/'decisions').mkdir(parents=True, exist_ok=True)
    (registry/'promotion_gates').mkdir(parents=True, exist_ok=True)
    (registry/'indexes').mkdir(parents=True, exist_ok=True)
    if not (registry/'registry.json').exists(): (registry/'registry.json').write_text(json.dumps({"entries":[]},indent=2),encoding='utf-8')

def update_ledger(input_path: Path, registry: Path):
    ensure_registry(registry)
    rec=json.loads(input_path.read_text(encoding='utf-8'))
    if rec.get('schema_version')=='securerails.human_review_request.v1':
        errs=validate_review_request(rec); kind='request'; rid=_required_id(rec, 'review_request_id'); out=_safe_out_path(registry, 'requests', rid)
    elif rec.get('schema_version')=='securerails.human_review_decision.v1':
        errs=validate_review_decision(rec); kind='decision'; rid=_required_id(rec, 'decision_id'); out=_safe_out_path(registry, 'decisions', rid)
    elif rec.get('schema_version')=='securerails.promotion_gate.v1':
        errs=validate_promotion_gate(rec); kind='promotion_gate'; rid=_required_id(rec, 'promotion_gate_id'); out=_safe_out_path(registry, 'promotion_gates', rid)
        source_decision_id = rec.get('source_decision_id')
        decision_file = _safe_out_path(registry, 'decisions', source_decision_id) if source_decision_id else None
        if not source_decision_id or not decision_file.exists():
            errs.append('source_decision_id must reference an existing decision record')
        else:
            decision = json.loads(decision_file.read_text(encoding='utf-8'))
            cond = rec.get('required_conditions', {})
            evidence = decision.get('evidence_reviewed', {})
            counters = decision.get('hard_safety_counters', {})
            promotion = decision.get('promotion', {})
            if cond.get('evidence_docket_present') is True and evidence.get('evidence_docket_reviewed') is not True:
                errs.append('gate/decision mismatch: evidence_docket_present')
            if cond.get('safety_ledger_present') is True and evidence.get('safety_ledger_reviewed') is not True:
                errs.append('gate/decision mismatch: safety_ledger_present')
            if cond.get('claim_boundary_present') is True and evidence.get('claim_boundary_reviewed') is not True:
                errs.append('gate/decision mismatch: claim_boundary_present')
            if cond.get('auto_merge_allowed') is False and promotion.get('auto_merge_allowed') is not False:
                errs.append('gate/decision mismatch: auto_merge_allowed')
            if cond.get('hard_safety_counters_zero') is True and any(int(v) != 0 for v in counters.values()):
                errs.append('gate/decision mismatch: hard_safety_counters_zero')
    else: raise ValueError('unsupported schema_version')
    if errs: raise ValueError('; '.join(errs))
    out.write_text(json.dumps(rec,indent=2),encoding='utf-8')
    reg=json.loads((registry/'registry.json').read_text())
    reg['entries'].append({'id':rid,'kind':kind,'path':str(out.relative_to(registry.resolve())),'updated_at':_now()})
    (registry/'registry.json').write_text(json.dumps(reg,indent=2),encoding='utf-8')
    (registry/'latest.json').write_text(json.dumps({'latest':reg['entries'][-1]},indent=2),encoding='utf-8')

def validate_ledger(registry: Path)->list[str]:
    errs=[]
    registry_file = registry/'registry.json'
    if not registry_file.exists():
        return ['missing registry.json']
    try:
        reg = json.loads(registry_file.read_text(encoding='utf-8'))
    except Exception as exc:
        return [f'invalid registry.json: {exc}']
    entries = reg.get('entries', [])
    if not isinstance(entries, list):
        return ['registry entries must be a list']
    for i, e in enumerate(entries):
        path = e.get('path')
        if not path:
            errs.append(f'entry[{i}] missing path')
            continue
        full = (registry / path).resolve()
        if registry.resolve() not in full.parents:
            errs.append(f'entry[{i}] path escapes registry')
            continue
        if not full.exists():
            errs.append(f'entry[{i}] missing file: {path}')
            continue
        try:
            rec = json.loads(full.read_text(encoding='utf-8'))
        except Exception as exc:
            errs.append(f'entry[{i}] invalid json: {exc}')
            continue
        sv = rec.get('schema_version')
        if sv == 'securerails.human_review_request.v1':
            errs.extend([f'entry[{i}] {m}' for m in validate_review_request(rec)])
        elif sv == 'securerails.human_review_decision.v1':
            errs.extend([f'entry[{i}] {m}' for m in validate_review_decision(rec)])
        elif sv == 'securerails.promotion_gate.v1':
            errs.extend([f'entry[{i}] {m}' for m in validate_promotion_gate(rec)])
        else:
            errs.append(f'entry[{i}] unsupported schema_version')
    return errs
