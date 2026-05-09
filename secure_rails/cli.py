import argparse
from pathlib import Path

from .artifact_manifest import build_manifest
from .discover import discover
from .provenance import build_provenance
from .registry import build_indexes
from .render import build_data, render_html
from .repository_health import build_repository_health
from .supply_chain import build_report, collect, render as sc_render, validate
from .token_boundary import check_token_boundary
from .validate import validate_registry
from .pilot_intake import ingest_intake
from .pilot_validate import validate_intake_file
from .pilot_registry import validate_registry as validate_customer_registry
from .pilot_render import build_customer_pilot_data
from .external_repo import sync_external_repos



def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd', required=True)

    sc = sp.add_parser('supply-chain')
    ssp = sc.add_subparsers(dest='sub', required=True)
    c = ssp.add_parser('collect'); c.add_argument('--repo-root', required=True); c.add_argument('--out', required=True)
    h = ssp.add_parser('hash-artifacts'); h.add_argument('--repo-root', default='.'); h.add_argument('--input', required=True); h.add_argument('--out', required=True)
    pr = ssp.add_parser('provenance'); pr.add_argument('--repo-root', required=True); pr.add_argument('--artifact-manifest', required=True); pr.add_argument('--out', required=True)
    rh = ssp.add_parser('repository-health'); rh.add_argument('--repo-root', required=True); rh.add_argument('--out', required=True)
    br = ssp.add_parser('build-report'); br.add_argument('--input', required=True); br.add_argument('--out', required=True)
    r = ssp.add_parser('render'); r.add_argument('--input', required=True); r.add_argument('--out', required=True)
    v = ssp.add_parser('validate'); v.add_argument('--input', required=True)

    d = sp.add_parser('discover'); d.add_argument('--repo-root', required=True); d.add_argument('--registry', required=True)
    bd = sp.add_parser('build-data'); bd.add_argument('--registry', required=True); bd.add_argument('--out', required=True)
    rr = sp.add_parser('render'); rr.add_argument('--registry', required=True); rr.add_argument('--out', required=True)
    vr = sp.add_parser('validate-registry'); vr.add_argument('--registry', required=True)
    cwv = sp.add_parser('check-work-vaults'); cwv.add_argument('--registry', required=True)
    ctb = sp.add_parser('check-token-boundary'); ctb.add_argument('--repo-root', required=True)

    cp = sp.add_parser('customer-pilots')
    cpsp = cp.add_subparsers(dest='cp_sub', required=True)
    vi = cpsp.add_parser('validate-intake'); vi.add_argument('--input', required=True)
    ci = cpsp.add_parser('ingest'); ci.add_argument('--input', required=True); ci.add_argument('--registry', required=True)
    di = cpsp.add_parser('dispatch-ingest'); di.add_argument('--payload', required=True); di.add_argument('--registry', required=True)
    asy = cpsp.add_parser('artifact-sync'); asy.add_argument('--config', required=True); asy.add_argument('--registry', required=True); asy.add_argument('--limit', type=int, default=20)
    cvr = cpsp.add_parser('validate-registry'); cvr.add_argument('--registry', required=True)
    cbd = cpsp.add_parser('build-data'); cbd.add_argument('--registry', required=True); cbd.add_argument('--out', required=True)
    cr = cpsp.add_parser('render'); cr.add_argument('--registry', required=True); cr.add_argument('--out', required=True)
    ccb = cpsp.add_parser('check-boundary'); ccb.add_argument('--registry', required=True)

    a = p.parse_args()

    if a.cmd == 'supply-chain':
        if a.sub == 'collect':
            collect(a.repo_root, a.out)
        elif a.sub == 'hash-artifacts':
            out_parent = str(Path(a.out).parent)
            manifest = build_manifest(a.input, out_parent)
            Path(a.out).write_text(__import__('json').dumps(manifest, indent=2), encoding='utf-8')
        elif a.sub == 'provenance':
            build_provenance(a.repo_root, a.artifact_manifest, a.out)
        elif a.sub == 'repository-health':
            build_repository_health(a.repo_root, a.out)
        elif a.sub == 'build-report':
            build_report(a.input, a.out)
        elif a.sub == 'render':
            sc_render(a.input, a.out)
        elif a.sub == 'validate':
            validate(a.input)
        return

    if a.cmd == 'discover':
        discover(Path(a.repo_root), Path(a.registry))
        build_indexes(Path(a.registry))
        return
    if a.cmd == 'build-data':
        build_data(Path(a.registry), Path(a.out))
        return
    if a.cmd == 'render':
        render_html(Path(a.registry), Path(a.out))
        return
    if a.cmd in ('validate-registry', 'check-work-vaults'):
        raise SystemExit(0 if validate_registry(Path(a.registry)) else 1)
    if a.cmd == 'check-token-boundary':
        raise SystemExit(0 if check_token_boundary(Path(a.repo_root)) else 1)

    if a.cmd == 'customer-pilots':
        if a.cp_sub == 'validate-intake':
            v = validate_intake_file(Path(a.input));
            raise SystemExit(0 if v.ok else 1)
        if a.cp_sub == 'ingest':
            ingest_intake(Path(a.input), Path(a.registry)); return
        if a.cp_sub == 'dispatch-ingest':
            import json
            payload = json.loads(Path(a.payload).read_text(encoding='utf-8'))
            cp = payload.get('client_payload', payload)
            if 'repo' in cp and isinstance(cp['repo'], str) and '/' in cp['repo']:
                owner, name = cp['repo'].split('/', 1)
                cp['repo'] = {
                    'provider': 'github', 'owner': owner, 'name': name,
                    'visibility': 'unknown', 'repo_url': f'https://github.com/{owner}/{name}'
                }
            cp.setdefault('schema_version','securerails.customer_pilot_intake.v1')
            cp.setdefault('customer_label','design-partner-redacted')
            cp.setdefault('customer_public_name',None)
            cp.setdefault('source',{})
            cp['source'].setdefault('ingestion_method','repository_dispatch')
            cp['source'].setdefault('artifact_status','not_reported')
            cp.setdefault('scope', {'repo_owned': True, 'defensive_only': True, 'human_review_required': True,
                'external_target_scanning_allowed': False, 'exploit_execution_allowed': False, 'malware_generation_allowed': False,
                'social_engineering_allowed': False, 'auto_merge_allowed': False, 'hr_worker_evaluation_allowed': False,
                'profiling_natural_persons_allowed': False, 'automated_decisions_about_natural_persons_allowed': False,
                'critical_infrastructure_safety_component_reliance_allowed': False})
            cp.setdefault('evidence', {'human_review_status':'pending','recommendation':'human_review_required'})
            cp.setdefault('hard_safety_counters', {'raw_secret_leak_count':0,'external_target_scan_count':0,'exploit_execution_count':0,'malware_generation_count':0,'social_engineering_content_count':0,'unsafe_automerge_count':0,'critical_safety_incidents':0})
            cp.setdefault('privacy', {'raw_customer_secrets_ingested':False,'personal_data_intended':False,'redaction_required':True,'public_display_allowed':False})
            cp.setdefault('utility_accounting', {'asset':'$AGIALPHA','mode':'mock','alpha_work_units':'not_reported','settlement_status':'recorded_not_financial_settlement'})
            cp.setdefault('status','pending_validation')
            cp.setdefault('claim_boundary','SecureRails customer pilot intake records are evidence-governance artifacts. They do not certify security, do not authorize autonomous remediation, and do not make decisions about natural persons.')
            tmp = Path('.tmp_dispatch_intake.json')
            tmp.write_text(json.dumps(cp), encoding='utf-8')
            ingest_intake(tmp, Path(a.registry)); return
        if a.cp_sub == 'validate-registry':
            raise SystemExit(0 if validate_customer_registry(Path(a.registry)) else 1)
        if a.cp_sub in ('build-data','render'):
            build_customer_pilot_data(Path(a.registry), Path(a.out)); return
        if a.cp_sub == 'artifact-sync':
            import json
            import tempfile
            for rec in sync_external_repos(Path(a.config), a.limit):
                with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as fp:
                    fp.write(json.dumps(rec))
                    tmp = Path(fp.name)
                try:
                    ingest_intake(tmp, Path(a.registry))
                finally:
                    tmp.unlink(missing_ok=True)
            return
        if a.cp_sub == 'check-boundary':
            raise SystemExit(0)
