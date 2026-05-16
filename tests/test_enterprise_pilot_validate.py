import json, subprocess, sys
from pathlib import Path

def test_smoke():
    out=Path('/tmp/enterprise-pilot-test')
    subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',str(out),'--workflow-family','software_quality_pack','--customer-mode','synthetic_only'])
    subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','validate','--run',str(out)])
    assert (out/'06_proofbundle.json').exists()
