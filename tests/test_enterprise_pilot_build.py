import json, tempfile, subprocess, sys
from pathlib import Path

def run_build(tmp):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])
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

def test_same_out_generates_new_run_id():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  first=json.loads(Path(d,'00_manifest.json').read_text(encoding='utf-8'))['run_id']
  run_build(d)
  second=json.loads(Path(d,'00_manifest.json').read_text(encoding='utf-8'))['run_id']
  assert first != second
