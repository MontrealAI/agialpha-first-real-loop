import tempfile, subprocess, sys, os, json

def test_settlement_is_utility_only():
    d=tempfile.mkdtemp()
    subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry",d+"/reg","--out",d])
    settlement=json.load(open(os.path.join(d,"settlement_receipt.json")))
    assert settlement["settlement_type"]=="utility-only"
    assert "receipt" in settlement
