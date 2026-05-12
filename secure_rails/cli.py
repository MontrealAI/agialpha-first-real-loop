import argparse
import json
import os
from pathlib import Path

from .discover import discover
from .registry import build_indexes
from .render import build_data as build_registry_data, render_html
from .token_boundary import check_token_boundary
from .e2e_canary import run_canary, replay, build_report, update_registry, build_data as canary_build_data, render, validate as canary_validate, list_fixtures_cmd
from .supply_chain import collect as sc_collect, build_report as sc_build_report, render as sc_render, validate as sc_validate

from .policy_kernel import load_kernel, validate_kernel, evaluate_file
from .policy_registry import write_decision_log
from .policy_render import build_data as build_policy_data
from .policy_opa_export import export_opa
from .validate import validate_registry
from .template_bootstrap import detect as tb_detect, init as tb_init, validate as tb_validate, health_check as tb_health_check, report as tb_report
from .repo_security_baseline import generate_baseline
from .trust_center import build_data as trust_build_data
from .release_train import build as rt_build, validate as rt_validate, marketplace as rt_marketplace, render_notes as rt_render_notes
from .pilot_validate import validate_intake_record
from .pilot_intake import ingest_intake
from .pilot_render import build_customer_pilot_data
from .github_app_permissions import validate_permissions_file
from .github_webhook_verify import verify_github_webhook_signature


def _validate_registry(registry: Path) -> int:
    required = [registry / 'indexes' / 'by_status.json', registry / 'indexes' / 'by_sovereign.json']
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        print('missing:', ', '.join(missing))
        return 1
    if not validate_registry(registry):
        return 1
    return 0


def main() -> None:
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd', required=True)

    d = sp.add_parser('discover'); d.add_argument('--repo-root', required=True); d.add_argument('--registry', required=True)
    r = sp.add_parser('render'); r.add_argument('--registry', required=True); r.add_argument('--out', required=True)
    b = sp.add_parser('build-data'); b.add_argument('--registry', required=True); b.add_argument('--out', required=True)
    vr = sp.add_parser('validate-registry'); vr.add_argument('--registry', required=True)
    cwv = sp.add_parser('check-work-vaults'); cwv.add_argument('--registry', required=True)

    t = sp.add_parser('check-token-boundary'); t.add_argument('--repo-root', default='.')
    gh = sp.add_parser('github-app'); ghsp = gh.add_subparsers(dest='gcmd', required=True); ghv=ghsp.add_parser('validate'); ghv.add_argument('--input', default='config/securerails_github_app_permissions.json'); ghw=ghsp.add_parser('verify-webhook'); ghw.add_argument('--secret-env', default='SECURERAILS_WEBHOOK_SECRET'); ghw.add_argument('--payload-file', required=True); ghw.add_argument('--signature', required=True)

    tb = sp.add_parser('template-bootstrap'); tbsp = tb.add_subparsers(dest='tcmd', required=True)
    tbd=tbsp.add_parser('detect'); tbd.add_argument('--repo-root', required=True); tbd.add_argument('--out', required=True)
    tbi=tbsp.add_parser('init'); tbi.add_argument('--repo-root', required=True); tbi.add_argument('--owner', required=True); tbi.add_argument('--repository', required=True); tbi.add_argument('--instance-name', required=True); tbi.add_argument('--instance-type', required=True); tbi.add_argument('--pages-url', default=''); tbi.add_argument('--out', required=True)
    tbv=tbsp.add_parser('validate'); tbv.add_argument('--repo-root', required=True); tbv.add_argument('--config', required=True)
    tbh=tbsp.add_parser('health-check'); tbh.add_argument('--repo-root', required=True); tbh.add_argument('--config', required=True); tbh.add_argument('--out', required=True)
    tbr=tbsp.add_parser('report'); tbr.add_argument('--repo-root', required=True); tbr.add_argument('--config', required=True); tbr.add_argument('--out', required=True)

    rp = sp.add_parser('repo-security'); rpsp = rp.add_subparsers(dest='rcmd', required=True)
    rpb=rpsp.add_parser('baseline'); rpb.add_argument('--repo-root', required=True); rpb.add_argument('--out', required=True)
    rpv=rpsp.add_parser('validate'); rpv.add_argument('--input', required=True)
    rpi=rpsp.add_parser('inventory'); rpi.add_argument('--repo-root', required=True); rpi.add_argument('--out', required=True)

    tr = sp.add_parser('trust-center'); trsp = tr.add_subparsers(dest='trcmd', required=True)
    trb=trsp.add_parser('build-data'); trb.add_argument('--repo-root', required=True); trb.add_argument('--out', required=True)

    rel = sp.add_parser('release-train'); relsp = rel.add_subparsers(dest='relcmd', required=True)
    relb=relsp.add_parser('build'); relb.add_argument('--repo-root', required=True); relb.add_argument('--release-version', required=True); relb.add_argument('--release-channel', required=True); relb.add_argument('--out', required=True)
    relm=relsp.add_parser('marketplace-readiness'); relm.add_argument('--repo-root', required=True); relm.add_argument('--out', required=True)
    reln=relsp.add_parser('render-notes'); reln.add_argument('--input', required=True); reln.add_argument('--out', required=True)
    relv=relsp.add_parser('validate'); relv.add_argument('--input', required=True)

    cp = sp.add_parser('customer-pilots'); cpsp = cp.add_subparsers(dest='cpcmd', required=True)
    cpv=cpsp.add_parser('validate-intake'); cpv.add_argument('--input', required=True)
    cpi=cpsp.add_parser('ingest'); cpi.add_argument('--input', required=True); cpi.add_argument('--registry', required=True)
    cpd=cpsp.add_parser('dispatch-ingest'); cpd.add_argument('--payload', required=True); cpd.add_argument('--registry', required=True)
    cpb=cpsp.add_parser('build-data'); cpb.add_argument('--registry', required=True); cpb.add_argument('--out', required=True)
    cpr=cpsp.add_parser('render'); cpr.add_argument('--registry', required=True); cpr.add_argument('--out', required=True)
    cpa=cpsp.add_parser('artifact-sync'); cpa.add_argument('--config', required=True); cpa.add_argument('--registry', required=True); cpa.add_argument('--limit', default='50')
    e = sp.add_parser('e2e-canary'); esp = e.add_subparsers(dest='ecmd', required=True)
    e_run = esp.add_parser('run'); e_run.add_argument('--repo-root', required=True); e_run.add_argument('--fixtures', required=True); e_run.add_argument('--out', required=True)
    e_replay = esp.add_parser('replay'); e_replay.add_argument('--input', required=True); e_replay.add_argument('--out', required=True)
    e_validate = esp.add_parser('validate'); e_validate.add_argument('--input', required=True)
    e_report = esp.add_parser('build-report'); e_report.add_argument('--input', required=True); e_report.add_argument('--out', required=True)
    e_reg = esp.add_parser('update-registry'); e_reg.add_argument('--input', required=True); e_reg.add_argument('--registry', required=True)
    e_data = esp.add_parser('build-data'); e_data.add_argument('--registry', required=True); e_data.add_argument('--out', required=True)
    e_render = esp.add_parser('render'); e_render.add_argument('--input', required=True); e_render.add_argument('--out', required=True)
    e_list = esp.add_parser('list-fixtures'); e_list.add_argument('--fixtures', required=True)

    s = sp.add_parser('supply-chain'); ssp = s.add_subparsers(dest='scmd', required=True)
    s_collect = ssp.add_parser('collect'); s_collect.add_argument('--repo-root', required=True); s_collect.add_argument('--out', required=True)
    s_hash = ssp.add_parser('hash-artifacts'); s_hash.add_argument('--input', required=True); s_hash.add_argument('--out', required=True)
    s_prov = ssp.add_parser('provenance'); s_prov.add_argument('--repo-root', required=True); s_prov.add_argument('--artifact-manifest', required=True); s_prov.add_argument('--out', required=True)
    s_health = ssp.add_parser('repository-health'); s_health.add_argument('--repo-root', required=True); s_health.add_argument('--out', required=True)
    s_brep = ssp.add_parser('build-report'); s_brep.add_argument('--input', required=True); s_brep.add_argument('--out', required=True)
    s_rend = ssp.add_parser('render'); s_rend.add_argument('--input', required=True); s_rend.add_argument('--out', required=True)
    s_val = ssp.add_parser('validate'); s_val.add_argument('--input', required=True)

    pol = sp.add_parser('policy'); psp = pol.add_subparsers(dest='pcmd', required=True)
    a = psp.add_parser('validate-kernel'); a.add_argument('--kernel', required=True)
    b2 = psp.add_parser('evaluate'); b2.add_argument('--input', required=True); b2.add_argument('--context-type', default='auto'); b2.add_argument('--out', required=True)
    c = psp.add_parser('evaluate-repo'); c.add_argument('--repo-root', required=True); c.add_argument('--out', required=True)
    d2 = psp.add_parser('decision-log'); d2.add_argument('--decisions', required=True); d2.add_argument('--registry', required=True)
    e2 = psp.add_parser('build-data'); e2.add_argument('--registry', required=True); e2.add_argument('--out', required=True)
    f = psp.add_parser('render'); f.add_argument('--registry', required=True); f.add_argument('--out', required=True)
    g = psp.add_parser('export-opa'); g.add_argument('--kernel', required=True); g.add_argument('--out', required=True)

    args = p.parse_args()
    if args.cmd == 'discover':
        discover(Path(args.repo_root), Path(args.registry)); build_indexes(Path(args.registry))
    elif args.cmd == 'build-data':
        build_registry_data(Path(args.registry), Path(args.out))
    elif args.cmd == 'render':
        render_html(Path(args.registry), Path(args.out))
    elif args.cmd == 'validate-registry':
        raise SystemExit(_validate_registry(Path(args.registry)))
    elif args.cmd == 'check-work-vaults':
        raise SystemExit(0 if validate_registry(Path(args.registry)) else 1)
    elif args.cmd == 'check-token-boundary':
        raise SystemExit(0 if check_token_boundary(Path(args.repo_root)) else 1)
    elif args.cmd == 'github-app':
        if args.gcmd == 'validate':
            ok, errs = validate_permissions_file(Path(args.input))
            if not ok:
                print('\n'.join(errs)); raise SystemExit(1)
        elif args.gcmd == 'verify-webhook':
            secret = os.environ.get(args.secret_env)
            if not secret:
                print(f'missing secret in env var: {args.secret_env}')
                raise SystemExit(1)
            payload = Path(args.payload_file).read_bytes()
            if not verify_github_webhook_signature(secret.encode('utf-8'), payload, args.signature):
                print('invalid webhook signature')
                raise SystemExit(1)
            print('ok')

    elif args.cmd == 'template-bootstrap':
        if args.tcmd == 'detect': tb_detect(Path(args.repo_root), Path(args.out))
        elif args.tcmd == 'init': tb_init(Path(args.repo_root), args.owner, args.repository, args.instance_name, args.instance_type, args.pages_url, Path(args.out))
        elif args.tcmd == 'validate':
            errs = tb_validate(Path(args.config))
            if errs:
                print('\n'.join(errs)); raise SystemExit(1)
        elif args.tcmd == 'health-check':
            health = tb_health_check(Path(args.repo_root), Path(args.config), Path(args.out))
            if health.get('status') != 'pass':
                raise SystemExit(1)
        elif args.tcmd == 'report': tb_report(Path(args.repo_root), Path(args.config), Path(args.out))
    elif args.cmd == 'repo-security':
        if args.rcmd == 'baseline': generate_baseline(args.repo_root, args.out)
        elif args.rcmd == 'validate':
            required = ['repo_security_baseline.json','dependency_inventory.json','code_scanning_readiness.json','secret_scanning_posture.json','sarif_ingestion_record.json','workflow_permission_review.json']
            missing = [n for n in required if not (Path(args.input) / n).exists()]
            if missing:
                print('missing: ' + ', '.join(missing))
                raise SystemExit(1)
        elif args.rcmd == 'inventory':
            from .dependency_inventory import collect_dependency_inventory
            Path(args.out).write_text(json.dumps(collect_dependency_inventory(Path(args.repo_root)), indent=2), encoding='utf-8')
    elif args.cmd == 'trust-center':
        if args.trcmd == 'build-data':
            status = trust_build_data(Path(args.repo_root), Path(args.out))
            checks = [status.get('claim_boundary_check'), status.get('safety_ledger_check'), status.get('no_automerge_check'), status.get('utility_token_boundary_check')]
            required_flags = [status.get('security_policy_present'), status.get('vulnerability_disclosure_present'), status.get('incident_response_runbook_present')]
            if any(c != 'pass' for c in checks) or any(v is not True for v in required_flags):
                raise SystemExit(1)
    elif args.cmd == 'release-train':
        if args.relcmd == 'build': rt_build(Path(args.repo_root), args.release_version, args.release_channel, Path(args.out))
        elif args.relcmd == 'marketplace-readiness': rt_marketplace(Path(args.repo_root), Path(args.out))
        elif args.relcmd == 'render-notes': rt_render_notes(Path(args.input), Path(args.out))
        elif args.relcmd == 'validate': rt_validate(Path(args.input))
    elif args.cmd == 'customer-pilots':
        if args.cpcmd == 'validate-intake':
            rec=json.loads(Path(args.input).read_text(encoding='utf-8')); vr=validate_intake_record(rec); print('ok' if vr.ok else 'invalid'); raise SystemExit(0 if vr.ok else 1)
        elif args.cpcmd == 'ingest': ingest_intake(Path(args.input), Path(args.registry))
        elif args.cpcmd == 'dispatch-ingest':
            payload = json.loads(Path(args.payload).read_text(encoding='utf-8'))
            cp = payload.get('client_payload', {})
            infile = cp.get('intake_file')
            if infile:
                ingest_intake(Path(infile), Path(args.registry))
            else:
                record = cp.get('intake_record') or cp
                if 'repo' in record and isinstance(record['repo'], str) and '/' in record['repo']:
                    owner, name = record['repo'].split('/', 1)
                else:
                    owner, name = 'unknown-owner', 'unknown-repo'
                normalized = {
                    'schema_version': 'securerails.customer_pilot_intake.v1',
                    'pilot_id': record.get('pilot_id', 'sr-pilot-dispatch-unknown'),
                    'customer_label': record.get('customer_label', 'design-partner-redacted'),
                    'repo': {'provider': 'github', 'owner': owner, 'name': name, 'repo_url': f'https://github.com/{owner}/{name}'},
                    'source': {'ingestion_method': 'repository_dispatch'},
                    'scope': {'repo_owned': True, 'defensive_only': True, 'human_review_required': True, 'external_target_scanning_allowed': False, 'exploit_execution_allowed': False, 'malware_generation_allowed': False, 'social_engineering_allowed': False, 'auto_merge_allowed': False, 'hr_worker_evaluation_allowed': False, 'profiling_natural_persons_allowed': False, 'automated_decisions_about_natural_persons_allowed': False, 'critical_infrastructure_safety_component_reliance_allowed': False},
                    'privacy': {'raw_customer_secrets_ingested': False},
                    'hard_safety_counters': {'raw_secret_leak_count': 0, 'external_target_scan_count': 0, 'exploit_execution_count': 0, 'malware_generation_count': 0, 'social_engineering_content_count': 0, 'unsafe_automerge_count': 0, 'critical_safety_incidents': 0},
                    'utility_accounting': {'asset': '$AGIALPHA'},
                    'claim_boundary': 'SecureRails customer pilot intake records are evidence-governance artifacts. They do not certify security, do not authorize autonomous remediation, and do not make decisions about natural persons.'
                }
                tmp = Path('/tmp/securerails-dispatch-intake.json')
                tmp.write_text(json.dumps(normalized, indent=2), encoding='utf-8')
                ingest_intake(tmp, Path(args.registry))
        elif args.cpcmd in {'build-data','render'}: build_customer_pilot_data(Path(args.registry), Path(args.out))
        elif args.cpcmd == 'artifact-sync':
            from .external_repo import sync_external_repos
            records = sync_external_repos(Path(args.config), int(args.limit))
            for i, rec in enumerate(records):
                tmp = Path(f'/tmp/securerails-artifact-sync-{i}.json')
                tmp.write_text(json.dumps(rec, indent=2), encoding='utf-8')
                ingest_intake(tmp, Path(args.registry))
            print(f'synced_records={len(records)}')
    elif args.cmd == 'e2e-canary':
        if args.ecmd == 'run': run_canary(Path(args.repo_root), Path(args.fixtures), Path(args.out))
        elif args.ecmd == 'replay':
            rep = replay(Path(args.input), Path(args.out))
            if not rep.get('replay_pass', False):
                raise SystemExit(1)
        elif args.ecmd == 'validate': canary_validate(Path(args.input))
        elif args.ecmd == 'build-report': build_report(Path(args.input), Path(args.out))
        elif args.ecmd == 'update-registry': update_registry(Path(args.input), Path(args.registry))
        elif args.ecmd == 'build-data': canary_build_data(Path(args.registry), Path(args.out))
        elif args.ecmd == 'render': render(Path(args.input), Path(args.out))
        elif args.ecmd == 'list-fixtures': list_fixtures_cmd(Path(args.fixtures))
    elif args.cmd == 'supply-chain':
        if args.scmd == 'collect': sc_collect(args.repo_root, args.out)
        elif args.scmd == 'hash-artifacts':
            from .artifact_manifest import build_manifest
            out_path = Path(args.out)
            manifest = build_manifest(args.input, str(out_path.parent))
            out_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        elif args.scmd == 'provenance':
            from .provenance import build_provenance
            build_provenance(args.repo_root, args.artifact_manifest, args.out)
        elif args.scmd == 'repository-health':
            from .repository_health import build_repository_health
            build_repository_health(args.repo_root, args.out)
        elif args.scmd == 'build-report': sc_build_report(args.input, args.out)
        elif args.scmd == 'render': sc_render(args.input, args.out)
        elif args.scmd == 'validate': sc_validate(args.input)
    elif args.cmd == 'policy':
        if args.pcmd == 'validate-kernel':
            errs = validate_kernel(load_kernel(args.kernel))
            if errs:
                print('\n'.join(errs)); raise SystemExit(1)
            print('kernel valid')
        elif args.pcmd == 'evaluate':
            Path(args.out).write_text(json.dumps(evaluate_file(args.input, args.context_type), indent=2), encoding='utf-8')
        elif args.pcmd == 'evaluate-repo':
            out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
            for stale in out.glob('decision_*.json'):
                stale.unlink()
            files = sorted([x for x in Path(args.repo_root).rglob('*') if x.is_file() and x.suffix.lower() in {'.md', '.json', '.yml', '.yaml'}])
            fail_decisions = 0
            for i, fp in enumerate(files):
                decision = evaluate_file(str(fp), 'auto')
                if decision.get('decision') in {'reject', 'quarantine'}:
                    fail_decisions += 1
                (out / f'decision_{i:04d}.json').write_text(json.dumps(decision, indent=2), encoding='utf-8')
            if fail_decisions:
                print(f'policy violations found: {fail_decisions}')
                raise SystemExit(1)
        elif args.pcmd == 'decision-log': write_decision_log(args.decisions, args.registry)
        elif args.pcmd in {'build-data', 'render'}: build_policy_data(args.registry, args.out)
        elif args.pcmd == 'export-opa': export_opa(args.kernel, args.out)


if __name__ == '__main__':
    main()
