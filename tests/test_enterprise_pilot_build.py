import subprocess,sys,tempfile,os

def test_build():
 d=tempfile.mkdtemp(); subprocess.check_call([sys.executable,'-m','agialpha_enterprise_pilot','build','--repo-root','.','--out',d,'--workflow-family','software_quality_pack','--customer-mode','synthetic_only']); assert os.path.exists(os.path.join(d,'01_pilot_intake.json'))
