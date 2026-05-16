import json, tempfile, subprocess, sys
from pathlib import Path

def run_build(tmp):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])

def run_build_with_registry(tmp, registry):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only','--registry',registry])
def test_build_creates_artifacts():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  assert Path(d,'06_proofbundle.json').exists()
  assert Path(d,'07_evidence_docket.json').exists()

def test_registry_is_append_only_across_runs():
 with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
  run_build(d1)
  run_build(d2)
  reg=json.loads(Path('enterprise_pilot_registry/registry.json').read_text(encoding='utf-8'))
  assert len(reg.get('runs',[])) >= 2
  pilot_intakes=json.loads(Path('enterprise_pilot_registry/pilot_intakes.json').read_text(encoding='utf-8'))
  assert len(pilot_intakes.get('records',[])) >= 2

def test_repeated_build_same_out_gets_new_run_id():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  r1=json.loads(Path(d,'00_manifest.json').read_text(encoding='utf-8'))['run_id']
  run_build(d)
  r2=json.loads(Path(d,'00_manifest.json').read_text(encoding='utf-8'))['run_id']
  assert r1 != r2

def test_pilot_outcome_registry_uses_stable_run_relative_path():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  outcomes=json.loads(Path('enterprise_pilot_registry/pilot_outcomes.json').read_text(encoding='utf-8'))
  rec=outcomes['records'][-1]
  assert rec['payload']['path'].startswith(f"runs/{rec['run_id']}/")

def test_build_supports_registry_override():
 with tempfile.TemporaryDirectory() as d:
  run_build_with_registry(d,'enterprise_pilot_registry_alt')
  assert Path('enterprise_pilot_registry_alt/registry.json').exists()

def test_stale_out_files_not_copied_to_registry_snapshot():
 with tempfile.TemporaryDirectory() as d:
  Path(d,'debug.tmp').write_text('stale',encoding='utf-8')
  run_build(d)
  latest=json.loads(Path('enterprise_pilot_registry/latest.json').read_text(encoding='utf-8'))
  run_id=latest['run_id']
  assert not Path(f'enterprise_pilot_registry/runs/{run_id}/debug.tmp').exists()
