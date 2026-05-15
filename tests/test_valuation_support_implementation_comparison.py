import json, subprocess, sys, tempfile, os

def test_has_30_axes():
    out=tempfile.mkdtemp()
    subprocess.check_call([sys.executable,'-m','agialpha_valuation_support','build','--repo-root','.','--ascension-registry','ascension_os_registry','--comparables','config/valuation_support_public_comparables.example.json','--market-context','config/valuation_support_market_context.example.json','--out',out])
    axes=json.load(open(os.path.join(out,'04_implementation_side_comparison.json')))['axes']
    assert len(axes)==30
