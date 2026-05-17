import pathlib, subprocess, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]

def test_discover():
  with tempfile.TemporaryDirectory() as td:
    reg=pathlib.Path(td)/"reg"
    subprocess.run(["python","-m","agialpha_engine","discover","--repo-root",str(ROOT),"--registry",str(reg)],check=True)
    assert (reg/"latest.json").exists()
