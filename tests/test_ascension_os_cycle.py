
import tempfile, pathlib, subprocess, sys

def test_run_cycle_creates_output():
    with tempfile.TemporaryDirectory() as d:
        out=pathlib.Path(d)/'run'; reg=pathlib.Path(d)/'reg'
        subprocess.check_call([sys.executable,'-m','agialpha_ascension_os','discover','--repo-root','.','--registry',str(reg)])
        subprocess.check_call([sys.executable,'-m','agialpha_ascension_os','run-cycle','--repo-root','.','--registry',str(reg),'--out',str(out)])
        assert (out/'17_proofbundle/proofbundle.json').exists()
        assert (out/'18_evidence_docket/00_manifest.json').exists()
