import json, os, subprocess, sys, tempfile


def test_build_data_emits_expected_generated_files():
    out = tempfile.mkdtemp()
    gen = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, "-m", "agialpha_valuation_support", "build", "--repo-root", ".", "--ascension-registry", "ascension_os_registry", "--comparables", "config/valuation_support_public_comparables.example.json", "--out", out])
    subprocess.check_call([sys.executable, "-m", "agialpha_valuation_support", "build-data", "--registry", "valuation_support_registry", "--out", gen])
    for name in ["latest.json", "summary.json", "implementation_comparison.json", "valuation_support_scorecard.json", "market_equivalence_sensitivity.json", "commercial_readiness.json", "moat_assessment.json", "risk_boundary.json"]:
        assert os.path.exists(os.path.join(gen, name))
