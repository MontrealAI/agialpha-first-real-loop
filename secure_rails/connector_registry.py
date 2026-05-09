
import json
from pathlib import Path
from uuid import uuid4

def _ensure(reg: Path):
    for d in ['installations','events','dispatches','indexes']:
        (reg/d).mkdir(parents=True, exist_ok=True)
    (reg/'registry.json').write_text(json.dumps({'schema_version':'securerails.connector_registry.v1'},indent=2),encoding='utf-8') if not (reg/'registry.json').exists() else None

def update_registry(input_path: Path, reg: Path):
    _ensure(reg)
    rec=json.loads(input_path.read_text(encoding='utf-8'))
    kind='events' if rec.get('schema_version')=='securerails.webhook_event.v1' else 'dispatches' if rec.get('schema_version')=='securerails.repository_dispatch_bridge.v1' else 'installations'
    rid=rec.get('event_id') or rec.get('installation_id') or rec.get('client_payload',{}).get('pilot_id') or f'record-{uuid4()}'
    (reg/kind/f'{rid}.json').write_text(json.dumps(rec,indent=2),encoding='utf-8')

def build_connector_data(reg: Path, out: Path):
    _ensure(reg); out.mkdir(parents=True, exist_ok=True)
    def load(d): return [json.loads(p.read_text()) for p in sorted((reg/d).glob('*.json'))]
    inst,ev,dis=load('installations'),load('events'),load('dispatches')
    (out/'installations.json').write_text(json.dumps(inst,indent=2),encoding='utf-8')
    (out/'events.json').write_text(json.dumps(ev,indent=2),encoding='utf-8')
    (out/'dispatches.json').write_text(json.dumps(dis,indent=2),encoding='utf-8')
    summary={'active_installations':sum(1 for i in inst if i.get('status')=='active'),'paused_installations':sum(1 for i in inst if i.get('status')=='paused'),'revoked_installations':sum(1 for i in inst if i.get('status')=='revoked'),'events_received':len(ev),'dispatch_payloads_built':len(dis),'dispatch_dry_runs':len(dis),'public_display_enabled_count':sum(1 for i in inst if i.get('public_display_allowed') is True),'private_only_count':sum(1 for i in inst if i.get('public_display_allowed') is not True)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
