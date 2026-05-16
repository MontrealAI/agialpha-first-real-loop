import subprocess,sys,tempfile

def test_validate():
 d=tempfile.mkdtemp(); subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',d,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only']); subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','validate','--run',d])
