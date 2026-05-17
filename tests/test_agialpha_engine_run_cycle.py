import pathlib, tempfile, subprocess, json

def test_run_cycle_minimum():
 d=tempfile.mkdtemp(); reg=tempfile.mkdtemp(); subprocess.check_call(["python","-m","agialpha_engine","discover","--repo-root",".","--registry",reg]); subprocess.check_call(["python","-m","agialpha_engine","run-cycle","--repo-root",".","--registry",reg,"--out",d,"--candidate-seeds","16","--evaluate-seeds","8","--sandbox-evals","4"]); seeds=json.loads(pathlib.Path(d,"02_generated_experiment_seeds.json").read_text()); assert len(seeds)==16
