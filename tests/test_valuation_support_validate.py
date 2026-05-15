import subprocess, sys, tempfile

def test_validate_passes():
    out=tempfile.mkdtemp()
    subprocess.check_call([sys.executable,'-m','agialpha_valuation_support','build','--repo-root','.','--ascension-registry','ascension_os_registry','--comparables','config/valuation_support_public_comparables.example.json','--market-context','config/valuation_support_market_context.example.json','--out',out])
    subprocess.check_call([sys.executable,'-m','agialpha_valuation_support','validate','--run',out])
