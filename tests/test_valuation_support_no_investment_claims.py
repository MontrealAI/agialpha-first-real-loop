import json, os, subprocess, sys, tempfile


def test_no_investment_claim_wording_present():
    out = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, "-m", "agialpha_valuation_support", "build", "--repo-root", ".", "--ascension-registry", "ascension_os_registry", "--comparables", "config/valuation_support_public_comparables.example.json", "--out", out])
    memo = open(os.path.join(out, "12_valuation_support_memo.md"), "r", encoding="utf-8").read().lower()
    assert "not investment advice" in memo
    assert "not assert a valuation" in memo
