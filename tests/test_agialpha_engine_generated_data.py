import subprocess, sys
from pathlib import Path

def run(*args): subprocess.check_call([sys.executable,'-m','agialpha_engine',*args])

def test_cycle(tmp_path):
 out=tmp_path/'run'; run('run-cycle','--repo-root','.','--registry','engine_registry','--out',str(out),'--candidate-tasks','16','--evaluate-tasks','6','--variants-per-task','2'); assert (out/'10_proofbundles/proofbundle.json').exists()
