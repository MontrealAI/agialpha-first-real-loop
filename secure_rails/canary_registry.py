import json
from pathlib import Path


def update_registry(input_dir: Path, registry_dir: Path):
    registry_dir.mkdir(parents=True, exist_ok=True)
    for p in ['runs', 'artifacts', 'indexes']:
        (registry_dir / p).mkdir(exist_ok=True)

    run = json.loads((input_dir / '00_manifest.json').read_text(encoding='utf-8'))
    reg_file = registry_dir / 'registry.json'
    if reg_file.exists():
        existing = json.loads(reg_file.read_text(encoding='utf-8'))
        runs = existing.get('runs', [])
    else:
        runs = []

    run_id = run.get('run_id')
    runs = [r for r in runs if r.get('run_id') != run_id]
    runs.append(run)

    reg = {"schema_version": "securerails.e2e_canary_registry.v1", "runs": runs}
    reg_file.write_text(json.dumps(reg, indent=2), encoding='utf-8')
    (registry_dir / 'latest.json').write_text(json.dumps(run, indent=2), encoding='utf-8')

    by_status = {}
    for r in runs:
        by_status.setdefault(r.get('status', 'unknown'), []).append(r.get('run_id'))
    (registry_dir / 'indexes/by_status.json').write_text(json.dumps(by_status, indent=2), encoding='utf-8')
    (registry_dir / 'indexes/by_fixture.json').write_text(json.dumps({}, indent=2), encoding='utf-8')
    (registry_dir / 'indexes/by_safety_status.json').write_text(json.dumps({"safe": [r.get('run_id') for r in runs]}, indent=2), encoding='utf-8')
    (registry_dir / 'CHANGELOG.md').write_text('# SecureRails Canary Registry\n', encoding='utf-8')


def build_data(registry_dir: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    latest = json.loads((registry_dir / 'latest.json').read_text(encoding='utf-8'))
    runs = json.loads((registry_dir / 'registry.json').read_text(encoding='utf-8')).get('runs', [])
    summary = {"latest_status": latest.get('status'), "run_count": len(runs)}
    (out_dir / 'latest.json').write_text(json.dumps(latest, indent=2), encoding='utf-8')
    (out_dir / 'runs.json').write_text(json.dumps(runs, indent=2), encoding='utf-8')
    (out_dir / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
