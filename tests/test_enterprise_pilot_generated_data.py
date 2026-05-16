import json, tempfile, subprocess, sys
from pathlib import Path

def run_build(tmp):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])
def test_generated_data():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build-data','--registry','enterprise_pilot_registry','--out','docs/_generated/enterprise-pilot'])
  assert Path('docs/_generated/enterprise-pilot/latest.json').exists()
