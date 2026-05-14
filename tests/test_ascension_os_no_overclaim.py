import tempfile, subprocess, sys, os

FORBIDDEN=["achieved AGI","achieved ASI","superintelligence","empirical SOTA","certified safe","EU AI Act exempt"]

def test_no_overclaim_in_outputs():
    d=tempfile.mkdtemp()
    subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry",d+"/reg","--out",d])
    blob="\n".join(open(os.path.join(d,f)).read() for f in os.listdir(d) if f.endswith(".json"))
    for bad in FORBIDDEN:
        assert bad not in blob
