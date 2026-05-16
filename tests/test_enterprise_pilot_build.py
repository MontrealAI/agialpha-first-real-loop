import json, tempfile, subprocess, sys
from pathlib import Path

def run_build(tmp):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])
def test_build_creates_artifacts():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  assert Path(d,'06_proofbundle.json').exists()
  assert Path(d,'07_evidence_docket.json').exists()
