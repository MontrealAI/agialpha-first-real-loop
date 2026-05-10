import json
from pathlib import Path

def update_registry(input_dir: Path, registry_dir: Path):
    registry_dir.mkdir(parents=True,exist_ok=True)
    for p in ['runs','artifacts','indexes']:
        (registry_dir/p).mkdir(exist_ok=True)
    run=json.loads((input_dir/'00_manifest.json').read_text())
    registry_file = registry_dir / 'registry.json'
    existing_runs = []
    if registry_file.exists():
        existing = json.loads(registry_file.read_text())
        existing_runs = existing.get('runs', []) if isinstance(existing, dict) else []

    runs_by_id = {r.get('run_id'): r for r in existing_runs if isinstance(r, dict) and r.get('run_id')}
    runs_by_id[run.get('run_id')] = run
    runs = sorted(runs_by_id.values(), key=lambda item: item.get('generated_at', ''))

    reg={"schema_version":"securerails.e2e_canary_registry.v1","runs":runs}
    registry_file.write_text(json.dumps(reg,indent=2))
    latest_run = runs[-1] if runs else run
    (registry_dir/'latest.json').write_text(json.dumps(latest_run,indent=2))
    by_status = {}
    by_safety = {}
    by_fixture = {}
    for item in runs:
        rid = item.get('run_id')
        if not rid:
            continue
        by_status.setdefault(item.get('status', 'unknown'), []).append(rid)
        counters = item.get('hard_safety_counters', {}) if isinstance(item.get('hard_safety_counters', {}), dict) else {}
        safety_key = 'safe' if all((counters.get(k, 0) == 0) for k in (
            'raw_secret_leak_count', 'external_target_scan_count', 'exploit_execution_count',
            'malware_generation_count', 'social_engineering_content_count', 'unsafe_automerge_count',
            'critical_safety_incidents'
        )) else 'incident'
        by_safety.setdefault(safety_key, []).append(rid)
        for fixture in item.get('fixtures', []):
            by_fixture.setdefault(str(fixture), []).append(rid)
    (registry_dir/'indexes/by_status.json').write_text(json.dumps(by_status,indent=2))
    (registry_dir/'indexes/by_fixture.json').write_text(json.dumps(by_fixture,indent=2))
    (registry_dir/'indexes/by_safety_status.json').write_text(json.dumps(by_safety,indent=2))
    (registry_dir/'CHANGELOG.md').write_text('# SecureRails Canary Registry\n', encoding='utf-8')

def build_data(registry_dir: Path, out_dir: Path):
    out_dir.mkdir(parents=True,exist_ok=True)
    latest=json.loads((registry_dir/'latest.json').read_text())
    runs=json.loads((registry_dir/'registry.json').read_text()).get('runs',[])
    summary={"latest_status":latest.get('status'),"run_count":len(runs)}
    (out_dir/'latest.json').write_text(json.dumps(latest,indent=2))
    (out_dir/'runs.json').write_text(json.dumps(runs,indent=2))
    (out_dir/'summary.json').write_text(json.dumps(summary,indent=2))
