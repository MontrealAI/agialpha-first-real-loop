import json, subprocess, sys, tempfile, os

def test_tier_cap_present():
    out=tempfile.mkdtemp(); subprocess.check_call([sys.executable,'-m','agialpha_valuation_support','build','--repo-root','.','--ascension-registry','ascension_os_registry','--comparables','config/valuation_support_public_comparables.example.json','--market-context','config/valuation_support_market_context.example.json','--out',out])
    d=json.load(open(os.path.join(out,'05_implementation_equivalence_score.json')))
    assert d['readiness_tier']=='T6'
