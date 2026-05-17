import json, pathlib, subprocess, tempfile

ROOT=pathlib.Path(__file__).resolve().parents[1]

def run_cycle(tmp):
    reg=tmp/'reg'; out=tmp/'run'
    subprocess.run(['python','-m','agialpha_engine','discover','--repo-root',str(ROOT),'--registry',str(reg)],check=True)
    subprocess.run(['python','-m','agialpha_engine','run-cycle','--repo-root',str(ROOT),'--registry',str(reg),'--out',str(out),'--candidate-seeds','16','--evaluate-seeds','8','--sandbox-evals','4'],check=True)
    return reg,out


def test_smoke_generated_data():
    with tempfile.TemporaryDirectory() as td:
        reg,out=run_cycle(pathlib.Path(td))
        assert out.exists()
