import json, tempfile, subprocess, sys
from pathlib import Path

def run_build(tmp):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])
def test_validate_passes():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','validate','--run',d])
