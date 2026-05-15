import json, subprocess, sys, tempfile, os

def test_arr_math():
    out=tempfile.mkdtemp(); subprocess.check_call([sys.executable,'-m','agialpha_valuation_support','build','--repo-root','.','--ascension-registry','ascension_os_registry','--comparables','config/valuation_support_public_comparables.example.json','--market-context','config/valuation_support_market_context.example.json','--out',out])
    d=json.load(open(os.path.join(out,'06_market_equivalence_sensitivity.json')))
    assert d['required_arr_by_multiple']['10']==465000000
    assert d['required_arr_by_multiple']['20']==232500000
    assert d['required_arr_by_multiple']['30']==155000000
    assert d['required_arr_by_multiple']['50']==93000000
