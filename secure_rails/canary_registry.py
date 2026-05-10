import json
from pathlib import Path

def update_registry(input_dir: Path, registry_dir: Path):
    registry_dir.mkdir(parents=True,exist_ok=True)
    for p in ['runs','artifacts','indexes']:
        (registry_dir/p).mkdir(exist_ok=True)
    report=json.loads((input_dir/'05_canary_report.json').read_text()) if (input_dir/'05_canary_report.json').exists() else json.loads((input_dir/'canary_report.json').read_text())
    run=json.loads((input_dir/'00_manifest.json').read_text())
    runs=[run]
    reg={"schema_version":"securerails.e2e_canary_registry.v1","runs":runs}
    (registry_dir/'registry.json').write_text(json.dumps(reg,indent=2))
    (registry_dir/'latest.json').write_text(json.dumps(run,indent=2))
    (registry_dir/'indexes/by_status.json').write_text(json.dumps({run['status']:[run['run_id']]},indent=2))
    (registry_dir/'indexes/by_fixture.json').write_text(json.dumps({},indent=2))
    (registry_dir/'indexes/by_safety_status.json').write_text(json.dumps({"safe":[run['run_id']]},indent=2))
    (registry_dir/'CHANGELOG.md').write_text('# SecureRails Canary Registry\n', encoding='utf-8')

def build_data(registry_dir: Path, out_dir: Path):
    out_dir.mkdir(parents=True,exist_ok=True)
    latest=json.loads((registry_dir/'latest.json').read_text())
    runs=json.loads((registry_dir/'registry.json').read_text()).get('runs',[])
    summary={"latest_status":latest.get('status'),"run_count":len(runs)}
    (out_dir/'latest.json').write_text(json.dumps(latest,indent=2))
    (out_dir/'runs.json').write_text(json.dumps(runs,indent=2))
    (out_dir/'summary.json').write_text(json.dumps(summary,indent=2))
