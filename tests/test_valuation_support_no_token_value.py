import json, os, subprocess, sys, tempfile


def test_no_token_value_claims():
    out = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, "-m", "agialpha_valuation_support", "build", "--repo-root", ".", "--ascension-registry", "ascension_os_registry", "--comparables", "config/valuation_support_public_comparables.example.json", "--out", out])
    claim = json.load(open(os.path.join(out, "00_manifest.json"), "r", encoding="utf-8"))["statement"].lower()
    assert "token-value claim" in claim
    assert "securities offering" in claim
