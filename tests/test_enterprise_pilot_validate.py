import json, tempfile, subprocess, sys
from pathlib import Path

def run_build(tmp):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])
def test_validate_passes():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','validate','--run',d])

def test_validate_rejects_forbidden_phrase_even_with_disclaimer_present():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  p=Path(d,'15_missing_evidence.json')
  p.write_text(p.read_text(encoding='utf-8')+'\n"not investment advice"\n"token appreciation"\n',encoding='utf-8')
  rc=subprocess.run([sys.executable,'-m','agialpha_enterprise_pilot','validate','--run',d],capture_output=True,text=True)
  assert rc.returncode != 0
  assert 'forbidden language' in (rc.stderr+rc.stdout).lower()
