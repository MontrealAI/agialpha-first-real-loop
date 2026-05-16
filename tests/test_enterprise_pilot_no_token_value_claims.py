import json, tempfile, subprocess, sys
from pathlib import Path

def run_build(tmp):
 subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',tmp,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])
def test_no_token_price():
 with tempfile.TemporaryDirectory() as d:
  run_build(d)
  t=Path(d,'09_utility_settlement_receipt.json').read_text().lower()
  assert 'token-value evidence' in t
