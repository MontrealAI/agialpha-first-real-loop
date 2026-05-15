import json, os, subprocess, sys, tempfile


def test_comparables_default_not_reported_preserved():
    out = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, "-m", "agialpha_valuation_support", "build", "--repo-root", ".", "--ascension-registry", "ascension_os_registry", "--comparables", "config/valuation_support_public_comparables.example.json", "--out", out])
    rows = json.load(open(os.path.join(out, "03_market_equivalence_sensitivity.json"), "r", encoding="utf-8"))["rows"]
    assert rows[0]["reported_category_valuation_comparable"] == "not_reported"
    assert rows[0]["scenario_multiples"] == "not_reported"
