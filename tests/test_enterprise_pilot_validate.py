import json, tempfile, subprocess, sys
from pathlib import Path
from agialpha_enterprise_pilot.validate import validate_run

def run_build(tmp):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])
def test_validate_passes():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','validate','--run',d])

def test_forbidden_phrase_not_waived_by_disclaimer():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  Path(d,'extra.md').write_text('not investment advice\nthis mentions token appreciation',encoding='utf-8')
  try:
   validate_run(Path(d))
   raise AssertionError('expected forbidden language failure')
  except SystemExit as e:
   assert 'forbidden language' in str(e)
