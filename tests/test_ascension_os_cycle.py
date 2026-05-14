import tempfile,subprocess,sys,os,json

def test_cycle_runs():
 d=tempfile.mkdtemp(); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry","ascension_os_registry","--out",d]); assert os.path.exists(os.path.join(d,"22_reports","ascension_scorecard.json"))

def test_passthrough_honors_out_path():
 d=tempfile.mkdtemp(); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-gauntlet","--repo-root",".","--out",d,"--task-count","3"]); assert os.path.exists(os.path.join(d,"run_gauntlet.json"))

def test_replay_fails_on_missing_run_dir():
 d=tempfile.mkdtemp(); rc=subprocess.run([sys.executable,"-m","agialpha_ascension_os","replay","--run",os.path.join(d,"missing")]); assert rc.returncode!=0

def test_validate_checks_reports():
 d=tempfile.mkdtemp(); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry","ascension_os_registry","--out",d]); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","replay","--run",d]); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","falsification-audit","--run",d]); subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","validate","--run",d]);
 data=json.load(open(os.path.join(d,"22_reports","validation_report.json"))); assert data["status"]=="pass"
