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
from .github_app_permissions import validate_permissions_file
from .github_webhook_verify import verify_github_webhook_signature
from .github_webhooks import normalize_webhook_payload
from .repository_dispatch_bridge import build_dispatch_from_webhook_event, validate_dispatch_payload
from .connector_intake import validate_installation_record
from .connector_registry import update_registry, build_connector_data
from .template_bootstrap import detect as tb_detect, init as tb_init, validate as tb_validate, health_check as tb_health_check, report as tb_report
from .release_train import build as rt_build, validate as rt_validate, marketplace as rt_marketplace, render_notes as rt_render_notes



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


    gha = sp.add_parser('github-app')
    ghsp = gha.add_subparsers(dest='gh_sub', required=True)
    vp = ghsp.add_parser('validate-permissions'); vp.add_argument('--input', required=True)
    ve = ghsp.add_parser('validate-events'); ve.add_argument('--input', required=True)
    vw = ghsp.add_parser('verify-webhook'); vw.add_argument('--secret-env', required=True); vw.add_argument('--payload-file', required=True); vw.add_argument('--signature', required=True)
    nw = ghsp.add_parser('normalize-webhook'); nw.add_argument('--payload-file', required=True); nw.add_argument('--event-type', required=True); nw.add_argument('--delivery-id', required=True); nw.add_argument('--out', required=True); nw.add_argument('--signature-verified', choices=['true','false'], default='false')
    bd2 = ghsp.add_parser('build-dispatch'); bd2.add_argument('--webhook-event', required=True); bd2.add_argument('--out', required=True)
    vd = ghsp.add_parser('validate-dispatch'); vd.add_argument('--input', required=True)
    vi2 = ghsp.add_parser('validate-installation'); vi2.add_argument('--input', required=True)
    ur = ghsp.add_parser('update-registry'); ur.add_argument('--input', required=True); ur.add_argument('--registry', required=True)
    bcd = ghsp.add_parser('build-data'); bcd.add_argument('--registry', required=True); bcd.add_argument('--out', required=True)

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

    tb = sp.add_parser('template-bootstrap')
    tbsp = tb.add_subparsers(dest='tb_sub', required=True)
    tbd = tbsp.add_parser('detect'); tbd.add_argument('--repo-root', required=True); tbd.add_argument('--out', required=True)
    tbi = tbsp.add_parser('init'); tbi.add_argument('--repo-root', required=True); tbi.add_argument('--owner', required=True); tbi.add_argument('--repository', required=True); tbi.add_argument('--instance-name', required=True); tbi.add_argument('--instance-type', required=True); tbi.add_argument('--pages-url', default=''); tbi.add_argument('--out', required=True)
    tbr = tbsp.add_parser('render'); tbr.add_argument('--repo-root', required=True); tbr.add_argument('--config', required=True); tbr.add_argument('--out', required=True)
    tbh = tbsp.add_parser('health-check'); tbh.add_argument('--repo-root', required=True); tbh.add_argument('--config', required=True); tbh.add_argument('--out', required=True)
    tbp = tbsp.add_parser('report'); tbp.add_argument('--repo-root', required=True); tbp.add_argument('--config', required=True); tbp.add_argument('--out', required=True)
    tbv = tbsp.add_parser('validate'); tbv.add_argument('--repo-root', required=True); tbv.add_argument('--config', required=True)

    rt = sp.add_parser('release-train')
    rtsp = rt.add_subparsers(dest='rt_sub', required=True)
    rtb=rtsp.add_parser('build'); rtb.add_argument('--repo-root', required=True); rtb.add_argument('--release-version', required=True); rtb.add_argument('--release-channel', required=True); rtb.add_argument('--out', required=True)
    rtv=rtsp.add_parser('validate'); rtv.add_argument('--input', required=True)
    rtm=rtsp.add_parser('marketplace-readiness'); rtm.add_argument('--repo-root', required=True); rtm.add_argument('--out', required=True)
    rtr=rtsp.add_parser('render-notes'); rtr.add_argument('--input', required=True); rtr.add_argument('--out', required=True)

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


    if a.cmd == 'github-app':
        import json, os
        if a.gh_sub == 'validate-permissions':
            ok, errs = validate_permissions_file(Path(a.input)); [print(e) for e in errs]; raise SystemExit(0 if ok else 1)
        if a.gh_sub == 'validate-events':
            data=json.loads(Path(a.input).read_text()); forbidden=set(data.get('forbidden_events',[])); default=set(data.get('default_allowed_events',[])); bad=sorted(forbidden & default); [print(f'forbidden event enabled by default: {b}') for b in bad]; raise SystemExit(0 if not bad else 1)
        if a.gh_sub == 'verify-webhook':
            payload=Path(a.payload_file).read_bytes(); secret_val=os.environ.get(a.secret_env);
            if not secret_val: print('webhook secret env var is unset or empty'); raise SystemExit(1)
            secret=secret_val.encode(); ok=verify_github_webhook_signature(secret,payload,a.signature); raise SystemExit(0 if ok else 1)
        if a.gh_sub == 'normalize-webhook':
            payload=json.loads(Path(a.payload_file).read_text()); verified=(a.signature_verified=='true'); out=normalize_webhook_payload(payload,a.event_type,a.delivery_id,verified); Path(a.out).write_text(json.dumps(out,indent=2)); return
        if a.gh_sub == 'build-dispatch':
            ev=json.loads(Path(a.webhook_event).read_text()); out=build_dispatch_from_webhook_event(ev); Path(a.out).write_text(json.dumps(out,indent=2)); return
        if a.gh_sub == 'validate-dispatch':
            d=json.loads(Path(a.input).read_text()); ok,errs=validate_dispatch_payload(d); [print(e) for e in errs]; raise SystemExit(0 if ok else 1)
        if a.gh_sub == 'validate-installation':
            d=json.loads(Path(a.input).read_text()); ok,errs=validate_installation_record(d); [print(e) for e in errs]; raise SystemExit(0 if ok else 1)
        if a.gh_sub == 'update-registry':
            update_registry(Path(a.input), Path(a.registry)); return
        if a.gh_sub == 'build-data':
            build_connector_data(Path(a.registry), Path(a.out)); return

    if a.cmd == 'template-bootstrap':
        repo_root = Path(a.repo_root)
        if a.tb_sub == 'detect':
            tb_detect(repo_root, Path(a.out)); return
        if a.tb_sub == 'init':
            tb_init(repo_root, a.owner, a.repository, a.instance_name, a.instance_type, a.pages_url, Path(a.out)); return
        if a.tb_sub == 'render':
            out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
            tb_report(repo_root, Path(a.config), out / 'setup_report.md'); return
        if a.tb_sub == 'health-check':
            health = tb_health_check(repo_root, Path(a.config), Path(a.out))
            raise SystemExit(0 if health.get('status') in ('pass', 'warning') else 1)
        if a.tb_sub == 'report':
            tb_report(repo_root, Path(a.config), Path(a.out)); return
        if a.tb_sub == 'validate':
            errs = tb_validate(Path(a.config)); [print(e) for e in errs]; raise SystemExit(0 if not errs else 1)

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

    if a.cmd == 'release-train':
        if a.rt_sub == 'build': rt_build(Path(a.repo_root), a.release_version, a.release_channel, Path(a.out)); return
        if a.rt_sub == 'validate': rt_validate(Path(a.input)); return
        if a.rt_sub == 'marketplace-readiness': rt_marketplace(Path(a.repo_root), Path(a.out)); return
        if a.rt_sub == 'render-notes': rt_render_notes(Path(a.input), Path(a.out)); return
