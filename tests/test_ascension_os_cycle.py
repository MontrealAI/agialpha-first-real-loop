import tempfile,subprocess,sys,os

def test_cycle_runs():
 d=tempfile.mkdtemp(); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry","ascension_os_registry","--out",d]); assert os.path.exists(os.path.join(d,"22_reports","ascension_scorecard.json"))
