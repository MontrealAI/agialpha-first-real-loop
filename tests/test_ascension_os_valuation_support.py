import tempfile, subprocess, sys, os, json

def test_valuation_support_builds_without_investment_claims():
    run=tempfile.mkdtemp(); out=tempfile.mkdtemp()
    subprocess.check_call([sys.executable,'-m','agialpha_ascension_os','run-cycle','--repo-root','.','--out',run])
    subprocess.check_call([sys.executable,'-m','agialpha_ascension_os','valuation-support','--repo-root','.','--run',run,'--out',out])
    data=json.load(open(os.path.join(out,'valuation_support.json')))
    assert 'not investment advice' in data['statement']
