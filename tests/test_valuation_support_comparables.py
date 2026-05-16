import json, os, subprocess, sys, tempfile


def test_comparables_default_not_reported_preserved():
    out = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, "-m", "agialpha_valuation_support", "build", "--repo-root", ".", "--ascension-registry", "ascension_os_registry", "--comparables", "config/valuation_support_public_comparables.example.json", "--out", out])
    sensitivity = json.load(open(os.path.join(out, "06_market_equivalence_sensitivity.json"), "r", encoding="utf-8"))
    assert sensitivity["target_comparable_valuation_usd"] == 4650000000
    assert sensitivity["required_arr_by_multiple"]["10"] == 465000000
