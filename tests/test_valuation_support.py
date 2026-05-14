import json, tempfile, subprocess, sys, os

def test_valuation_support_build_and_validate():
    d=tempfile.mkdtemp(); out=tempfile.mkdtemp()
    subprocess.check_call([sys.executable,"-m","agialpha_ascension_os","run-cycle","--repo-root",".","--registry","ascension_os_registry","--out",d])
    subprocess.check_call([sys.executable,"-m","agialpha_valuation_support","build","--repo-root",".","--ascension-registry","ascension_os_registry","--comparables","config/valuation_support_public_comparables.example.json","--out",out])
    subprocess.check_call([sys.executable,"-m","agialpha_valuation_support","validate","--run",out])
    data=json.load(open(os.path.join(out,'00_manifest.json')))
    s=data['statement'].lower()
    assert 'not investment advice' in s and 'fair-market-value opinion' in data['statement']
