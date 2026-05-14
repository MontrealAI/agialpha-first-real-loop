
import tempfile,subprocess,sys,os

def test_cycle_runs():
 d=tempfile.mkdtemp(); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry","ascension_os_registry","--out",d]); assert os.path.exists(os.path.join(d,"22_reports","ascension_scorecard.json"))

def test_passthrough_honors_out_path():
 d=tempfile.mkdtemp(); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-gauntlet","--repo-root",".","--out",d,"--task-count","3"]); assert os.path.exists(os.path.join(d,"run_gauntlet.json"))

def test_falsification_fails_on_missing_run():
 d=tempfile.mkdtemp();
 rc=subprocess.run([sys.executable,"-m","agialpha_ascension_os","falsification-audit","--run",os.path.join(d,"missing")],capture_output=True)
 assert rc.returncode != 0
