import json
import re
from pathlib import Path
from datetime import datetime, timezone
from .review_request import validate_review_request
from .review_decision import validate_review_decision
from .human_review import validate_promotion_gate

def _now(): return datetime.now(timezone.utc).isoformat()
_SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")

def _validate_id(value: str, field: str) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return [f"{field} must be a non-empty string"]
    if not _SAFE_ID.fullmatch(value):
        return [f"{field} contains unsafe characters"]
    return []

def _safe_out_path(registry: Path, subdir: str, rid: str) -> Path:
    out = (registry / subdir / f"{rid}.json").resolve()
    root = registry.resolve()
    if root not in out.parents:
        raise ValueError("ledger output path escapes registry")
    return out

def ensure_registry(registry: Path):
    (registry/'requests').mkdir(parents=True, exist_ok=True)
    (registry/'decisions').mkdir(parents=True, exist_ok=True)
    (registry/'promotion_gates').mkdir(parents=True, exist_ok=True)
    (registry/'indexes').mkdir(parents=True, exist_ok=True)
    if not (registry/'registry.json').exists(): (registry/'registry.json').write_text(json.dumps({"entries":[]},indent=2),encoding='utf-8')

def update_ledger(input_path: Path, registry: Path):
    ensure_registry(registry)
    registry = registry.resolve()
    rec=json.loads(input_path.read_text(encoding='utf-8'))
    if rec.get('schema_version')=='securerails.human_review_request.v1':
        errs=validate_review_request(rec); kind='request'; rid=rec.get('review_request_id','unknown'); errs.extend(_validate_id(rid, "review_request_id")); out=_safe_out_path(registry, 'requests', rid)
    elif rec.get('schema_version')=='securerails.human_review_decision.v1':
        errs=validate_review_decision(rec); kind='decision'; rid=rec.get('decision_id','unknown'); errs.extend(_validate_id(rid, "decision_id")); out=_safe_out_path(registry, 'decisions', rid)
    elif rec.get('schema_version')=='securerails.promotion_gate.v1':
        errs=validate_promotion_gate(rec); kind='promotion_gate'; rid=rec.get('promotion_gate_id','unknown'); errs.extend(_validate_id(rid, "promotion_gate_id")); out=_safe_out_path(registry, 'promotion_gates', rid)
        source_decision_id = rec.get('source_decision_id')
        errs.extend(_validate_id(source_decision_id, "source_decision_id"))
        decision_file = _safe_out_path(registry, 'decisions', source_decision_id) if not errs else registry / 'decisions' / 'invalid.json'
        if not source_decision_id or not decision_file.exists():
            errs.append('source_decision_id must reference an existing decision record')
        else:
            decision = json.loads(decision_file.read_text(encoding='utf-8'))
            d_prom = decision.get("promotion", {})
            d_ev = decision.get("evidence_reviewed", {})
            d_cnt = decision.get("hard_safety_counters", {})
            cond = rec.get("required_conditions", {})
            if cond.get("auto_merge_allowed") is not (d_prom.get("auto_merge_allowed") is True):
                errs.append("gate auto_merge_allowed contradicts source decision")
            if cond.get("evidence_docket_present") is not (d_ev.get("evidence_docket_reviewed") is True):
                errs.append("gate evidence_docket_present contradicts source decision")
            all_zero = all(int(v) == 0 for v in d_cnt.values()) if isinstance(d_cnt, dict) and d_cnt else False
            if cond.get("hard_safety_counters_zero") is not all_zero:
                errs.append("gate hard_safety_counters_zero contradicts source decision")
    else: raise ValueError('unsupported schema_version')
    if errs: raise ValueError('; '.join(errs))
    out.write_text(json.dumps(rec,indent=2),encoding='utf-8')
    reg=json.loads((registry/'registry.json').read_text())
    reg['entries'].append({'id':rid,'kind':kind,'path':str(out.relative_to(registry)),'updated_at':_now()})
    (registry/'registry.json').write_text(json.dumps(reg,indent=2),encoding='utf-8')
    (registry/'latest.json').write_text(json.dumps({'latest':reg['entries'][-1]},indent=2),encoding='utf-8')

def validate_ledger(registry: Path)->list[str]:
    errs=[]
    reg_file = registry / 'registry.json'
    if not reg_file.exists():
        errs.append('missing registry.json')
        return errs
    try:
        reg = json.loads(reg_file.read_text(encoding='utf-8'))
    except Exception as ex:
        return [f'invalid registry.json: {ex}']
    entries = reg.get("entries", [])
    if not isinstance(entries, list):
        return ["registry entries must be a list"]
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errs.append(f'entry[{i}] must be object'); continue
        p = entry.get("path")
        kind = entry.get("kind")
        if kind not in {"request","decision","promotion_gate"}:
            errs.append(f'entry[{i}] invalid kind')
        if not isinstance(p, str):
            errs.append(f'entry[{i}] missing path'); continue
        fp = (registry / p).resolve()
        if registry.resolve() not in fp.parents or not fp.exists():
            errs.append(f'entry[{i}] missing file: {p}'); continue
        try:
            rec = json.loads(fp.read_text(encoding='utf-8'))
        except Exception as ex:
            errs.append(f'entry[{i}] invalid json: {ex}'); continue
        if kind == "request":
            rerr = validate_review_request(rec)
        elif kind == "decision":
            rerr = validate_review_decision(rec)
        else:
            rerr = validate_promotion_gate(rec)
        if rerr:
            errs.append(f'entry[{i}] invalid record: {"; ".join(rerr)}')
    return errs
